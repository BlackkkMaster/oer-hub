from django.conf import settings
from django.contrib.auth.models import (
    AbstractUser,
    UserManager as BaseUserManager,
)
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    def normalize_email(self, email):
        if not email or "@" not in email:
            return email
        email = super().normalize_email(email).lower()
        local_part, domain = email.split("@", 1)
        local_part = local_part.split("+")[0]
        if domain in ["google.com", "googlemail.com", "gmail.com"]:
            domain = "gmail.com"
            local_part = local_part.replace(".", "")
        elif domain in ["ya.ru", "yandex.ru"]:
            domain = "yandex.ru"
            local_part = local_part.replace(".", "-")
        return f"{local_part}@{domain}"

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def by_mail(self, email):
        return self.active().get(email=self.normalize_email(email))


class User(AbstractUser):
    email = models.EmailField(
        verbose_name="электронная почта",
        unique=True,
    )

    objects = UserManager()

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.username


class Role(models.TextChoices):
    STUDENT = "student", "Студент"
    TEACHER = "teacher", "Преподаватель"
    ADMIN = "admin", "Администратор"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="пользователь",
    )
    role = models.CharField(
        verbose_name="роль",
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )
    department = models.CharField(
        verbose_name="кафедра",
        max_length=255,
        blank=True,
    )
    bio = models.TextField(
        verbose_name="о себе",
        blank=True,
    )
    git_username = models.CharField(
        verbose_name="имя пользователя в Git",
        max_length=150,
        blank=True,
    )
    attempts_count = models.PositiveIntegerField(
        verbose_name="число попыток входа",
        default=0,
    )

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        role = Role.ADMIN if instance.is_superuser else Role.STUDENT
        Profile.objects.create(user=instance, role=role)
