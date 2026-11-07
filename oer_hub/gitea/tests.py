from django.test import SimpleTestCase

from gitea.client import GiteaClient


class GiteaClientTests(SimpleTestCase):
    def test_client_init_and_urls(self):
        client = GiteaClient(
            base_url="http://git.local:3000",
            token="test-token",
        )
        self.assertEqual(client.base_url, "http://git.local:3000")
        self.assertEqual(client.api_url, "http://git.local:3000/api/v1")
        self.assertEqual(client.token, "test-token")
        headers = client._get_headers()
        self.assertIn("Authorization", headers)
        self.assertEqual(headers["Authorization"], "token test-token")
