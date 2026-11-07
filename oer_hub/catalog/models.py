from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.models import NamedModel, TimeStampedModel


class Semester(NamedModel):
    number = models.PositiveSmallIntegerField(
        verbose_name="номер семестра",
        unique=True,
    )
    is_active = models.BooleanField(
        verbose_name="активен",
        default=True,
    )

    class Meta:
        verbose_name = "семестр"
        verbose_name_plural = "семестры"
        ordering = ["number"]


class Discipline(NamedModel):
    code = models.CharField(
        verbose_name="код дисциплины",
        max_length=50,
        blank=True,
    )
    description = models.TextField(
        verbose_name="описание",
        blank=True,
    )

    class Meta:
        verbose_name = "дисциплина"
        verbose_name_plural = "дисциплины"
        ordering = ["name"]


class Course(NamedModel):
    slug = models.SlugField(
        verbose_name="идентификатор (slug)",
        max_length=100,
        unique=True,
    )
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.PROTECT,
        related_name="courses",
        verbose_name="дисциплина",
    )
    semester = models.ForeignKey(
        Semester,
        on_delete=models.PROTECT,
        related_name="courses",
        verbose_name="семестр",
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="taught_courses",
        verbose_name="преподаватель",
    )
    description = models.TextField(
        verbose_name="описание курса",
        blank=True,
    )
    is_published = models.BooleanField(
        verbose_name="опубликован",
        default=True,
    )
    git_repository_url = models.URLField(
        verbose_name="ссылка на репозиторий Git",
        blank=True,
    )
    git_clone_url = models.CharField(
        verbose_name="URL клонирования Git",
        max_length=500,
        blank=True,
    )

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ["semester", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=False)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:course_detail", kwargs={"slug": self.slug})


class Material(TimeStampedModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="materials",
        verbose_name="курс",
    )
    title = models.CharField(
        verbose_name="название материала",
        max_length=255,
    )
    description = models.TextField(
        verbose_name="описание",
        blank=True,
    )
    file = models.FileField(
        verbose_name="файл материала",
        upload_to="materials/%Y/%m/",
        blank=True,
    )
    release_version = models.CharField(
        verbose_name="версия релиза",
        max_length=50,
        default="v1.0.0",
    )

    class Meta:
        verbose_name = "материал"
        verbose_name_plural = "материалы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.release_version})"
