from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="дата обновления"),
                ),
                ("name", models.CharField(max_length=255, verbose_name="название")),
                (
                    "slug",
                    models.SlugField(
                        max_length=100, unique=True, verbose_name="идентификатор (slug)"
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="описание курса"),
                ),
                (
                    "is_published",
                    models.BooleanField(default=True, verbose_name="опубликован"),
                ),
                (
                    "git_repository_url",
                    models.URLField(
                        blank=True, verbose_name="ссылка на репозиторий Git"
                    ),
                ),
                (
                    "git_clone_url",
                    models.CharField(
                        blank=True, max_length=500, verbose_name="URL клонирования Git"
                    ),
                ),
            ],
            options={
                "verbose_name": "курс",
                "verbose_name_plural": "курсы",
                "ordering": ["semester", "name"],
            },
        ),
        migrations.CreateModel(
            name="Discipline",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="дата обновления"),
                ),
                ("name", models.CharField(max_length=255, verbose_name="название")),
                (
                    "code",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="код дисциплины"
                    ),
                ),
                ("description", models.TextField(blank=True, verbose_name="описание")),
            ],
            options={
                "verbose_name": "дисциплина",
                "verbose_name_plural": "дисциплины",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Material",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="дата обновления"),
                ),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="название материала"),
                ),
                ("description", models.TextField(blank=True, verbose_name="описание")),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        upload_to="materials/%Y/%m/",
                        verbose_name="файл материала",
                    ),
                ),
                (
                    "release_version",
                    models.CharField(
                        default="v1.0.0", max_length=50, verbose_name="версия релиза"
                    ),
                ),
            ],
            options={
                "verbose_name": "материал",
                "verbose_name_plural": "материалы",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Semester",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="дата обновления"),
                ),
                ("name", models.CharField(max_length=255, verbose_name="название")),
                (
                    "number",
                    models.PositiveSmallIntegerField(
                        unique=True, verbose_name="номер семестра"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="активен"),
                ),
            ],
            options={
                "verbose_name": "семестр",
                "verbose_name_plural": "семестры",
                "ordering": ["number"],
            },
        ),
    ]
