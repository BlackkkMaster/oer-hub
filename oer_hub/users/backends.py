from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        try:
            if "@" in str(username):
                user = User.objects.by_mail(username)
            else:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            if hasattr(user, "profile"):
                user.profile.attempts_count = 0
                user.profile.save(update_fields=["attempts_count"])
            return user

        if hasattr(user, "profile"):
            user.profile.attempts_count += 1
            user.profile.save(update_fields=["attempts_count"])
        return None
