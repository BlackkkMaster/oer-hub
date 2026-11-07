from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class HomepageTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage_status_code(self):
        response = self.client.get(reverse("homepage:index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_homepage_template_used(self):
        response = self.client.get(reverse("homepage:index"))
        self.assertTemplateUsed(response, "homepage/index.html")
        self.assertTemplateUsed(response, "base.html")
