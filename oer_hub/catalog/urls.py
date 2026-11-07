from django.urls import path

from catalog.views import CourseCreateView, CourseDetailView, CourseListView

app_name = "catalog"

urlpatterns = [
    path("", CourseListView.as_view(), name="course_list"),
    path("create/", CourseCreateView.as_view(), name="course_create"),
    path("<slug:slug>/", CourseDetailView.as_view(), name="course_detail"),
]
