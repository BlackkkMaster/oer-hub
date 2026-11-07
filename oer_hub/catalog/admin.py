from django.contrib import admin

from catalog.models import Course, Discipline, Material, Semester


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("number", "name", "is_active")
    list_editable = ("is_active",)


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


class MaterialInline(admin.TabularInline):
    model = Material
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "discipline",
        "semester",
        "teacher",
        "is_published",
        "git_repository_url",
    )
    list_filter = ("semester", "discipline", "is_published")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [MaterialInline]


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "release_version", "created_at")
    list_filter = ("course__semester", "release_version")
    search_fields = ("title", "course__name")
