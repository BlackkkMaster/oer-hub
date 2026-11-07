from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import Course, Discipline, Semester

User = get_user_model()


class CatalogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(
            username="testteacher",
            email="teacher@test.com",
            password="testpassword123",
        )
        self.semester = Semester.objects.create(name="Семестр 1", number=1)
        self.discipline = Discipline.objects.create(
            name="Программирование", code="CS101"
        )
        self.course = Course.objects.create(
            name="Введение в Python",
            slug="intro-to-python",
            discipline=self.discipline,
            semester=self.semester,
            teacher=self.teacher,
            description="Базовый курс по Python",
            is_published=True,
        )

    def test_course_list_status_code(self):
        response = self.client.get(reverse("catalog:course_list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "catalog/course_list.html")
        self.assertContains(response, self.course.name)

    def test_course_detail_status_code(self):
        response = self.client.get(
            reverse("catalog:course_detail", kwargs={"slug": self.course.slug})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "catalog/course_detail.html")
        self.assertContains(response, self.course.name)

    def test_course_detail_not_found(self):
        response = self.client.get(
            reverse("catalog:course_detail", kwargs={"slug": "non-existent"})
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_course_create_requires_login(self):
        response = self.client.get(reverse("catalog:course_create"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn(reverse("users:login"), response.headers["Location"])
