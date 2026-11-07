from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


class TitleMixin:
    title = ""

    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_title()
        return context


class RoleRequiredMixin(AccessMixin):
    allowed_roles = ()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        profile = getattr(request.user, "profile", None)
        if not profile or profile.role not in self.allowed_roles:
            if not request.user.is_superuser:
                raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class TeacherRequiredMixin(RoleRequiredMixin):
    allowed_roles = ("teacher", "admin")
