from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from users.models import Profile, Role

User = get_user_model()


class SignupForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=Role.choices,
        label="Роль",
        initial=Role.STUDENT,
    )
    department = forms.CharField(
        max_length=255,
        required=False,
        label="Кафедра",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile = getattr(user, "profile", None)
            if profile:
                profile.role = self.cleaned_data["role"]
                profile.department = self.cleaned_data["department"]
                profile.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("department", "bio", "git_username")
