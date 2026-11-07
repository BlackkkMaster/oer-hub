from core.mixins import TeacherRequiredMixin, TitleMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from gitea.services import sync_course_repository

from catalog.models import Course, Semester


class CourseListView(TitleMixin, ListView):
    model = Course
    template_name = "catalog/course_list.html"
    context_object_name = "courses"
    title = "Каталог курсов"

    def get_queryset(self):
        queryset = (
            Course.objects.filter(is_published=True)
            .select_related("discipline", "semester", "teacher")
            .prefetch_related("materials")
        )
        semester_id = self.request.GET.get("semester")
        if semester_id and semester_id.isdigit():
            queryset = queryset.filter(semester_id=semester_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["semesters"] = Semester.objects.filter(is_active=True)
        context["selected_semester"] = self.request.GET.get("semester")
        return context


class CourseDetailView(TitleMixin, DetailView):
    model = Course
    template_name = "catalog/course_detail.html"
    context_object_name = "course"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_title(self):
        return self.object.name

    def get_queryset(self):
        return (
            Course.objects.all()
            .select_related("discipline", "semester", "teacher")
            .prefetch_related("materials")
        )


class CourseCreateView(
    LoginRequiredMixin, TeacherRequiredMixin, TitleMixin, CreateView
):
    model = Course
    fields = (
        "name",
        "slug",
        "discipline",
        "semester",
        "description",
        "is_published",
    )
    template_name = "catalog/course_form.html"
    title = "Создание курса"
    success_url = reverse_lazy("catalog:course_list")

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        response = super().form_valid(form)
        try:
            sync_course_repository(self.object)
            messages.success(self.request, "Курс и репозиторий в Git успешно созданы!")
        except Exception as exc:
            messages.warning(
                self.request,
                f"Курс сохранен, но ошибка при создании Git-репозитория: {exc}",
            )
        return response
