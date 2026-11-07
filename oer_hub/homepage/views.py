from django.views.generic import TemplateView

from catalog.models import Course, Semester
from core.mixins import TitleMixin


class HomeView(TitleMixin, TemplateView):
    template_name = "homepage/index.html"
    title = "Кафедральный репозиторий образовательных ресурсов"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_courses"] = (
            Course.objects.filter(is_published=True)
            .select_related("discipline", "semester", "teacher")
            .order_by("-created_at")[:6]
        )
        context["active_semesters"] = Semester.objects.filter(is_active=True)
        return context
