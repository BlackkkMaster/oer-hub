from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from core.mixins import TitleMixin
from users.forms import ProfileUpdateForm, SignupForm, UserUpdateForm


class UserLoginView(TitleMixin, LoginView):
    template_name = "users/login.html"
    title = "Вход в систему"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("homepage:index")


class SignupView(TitleMixin, CreateView):
    form_class = SignupForm
    template_name = "users/signup.html"
    title = "Регистрация"
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object, backend="users.backends.AuthBackend")
        return response


class ProfileView(LoginRequiredMixin, TitleMixin, TemplateView):
    template_name = "users/profile.html"
    title = "Профиль пользователя"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user_form"] = kwargs.get("user_form") or UserUpdateForm(
            instance=user
        )
        context["profile_form"] = kwargs.get(
            "profile_form"
        ) or ProfileUpdateForm(instance=getattr(user, "profile", None))
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(
            request.POST, instance=getattr(user, "profile", None)
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("users:profile")
        return self.render_to_response(
            self.get_context_data(
                user_form=user_form, profile_form=profile_form
            )
        )
