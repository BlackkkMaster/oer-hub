import os
from typing import Any, Optional

import httpx


class GiteaAPIError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Any] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class GiteaClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        admin_username: Optional[str] = None,
        admin_password: Optional[str] = None,
    ):
        self.base_url = (base_url or os.getenv("GITEA_URL", "http://localhost:3000")).rstrip("/")
        self.api_url = f"{self.base_url}/api/v1"
        self.token = token or os.getenv("GITEA_ADMIN_TOKEN", "")
        self.admin_username = admin_username or os.getenv("GITEA_ADMIN_USERNAME", "gitea_admin")
        self.admin_password = admin_password or os.getenv("GITEA_ADMIN_PASSWORD", "gitea_admin_password")

    def _get_headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers

    def _get_auth(self) -> Optional[tuple[str, str]]:
        if not self.token and self.admin_username and self.admin_password:
            return (self.admin_username, self.admin_password)
        return None

    def _request(self, method: str, path: str, **kwargs) -> Any:
        url = f"{self.api_url}{path}"
        headers = self._get_headers()
        auth = self._get_auth()

        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    auth=auth,
                    **kwargs,
                )
        except httpx.RequestError as exc:
            raise GiteaAPIError(f"Network error connecting to Gitea: {exc}") from exc

        if response.status_code >= 400:
            raise GiteaAPIError(
                f"Gitea API error {response.status_code}: {response.text}",
                status_code=response.status_code,
                response=response,
            )

        if response.status_code == 204 or not response.content:
            return {}
        return response.json()

    def get_version(self) -> dict[str, Any]:
        return self._request("GET", "/version")

    def get_organization(self, org: str) -> dict[str, Any]:
        return self._request("GET", f"/orgs/{org}")

    def create_organization(self, name: str, description: str = "") -> dict[str, Any]:
        payload = {
            "username": name,
            "full_name": name,
            "description": description,
            "visibility": "public",
        }
        return self._request("POST", "/orgs", json=payload)

    def ensure_organization(self, name: str, description: str = "") -> dict[str, Any]:
        try:
            return self.get_organization(name)
        except GiteaAPIError as exc:
            if exc.status_code == 404:
                return self.create_organization(name, description)
            raise

    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        must_change_password: bool = False,
    ) -> dict[str, Any]:
        payload = {
            "username": username,
            "email": email,
            "password": password,
            "must_change_password": must_change_password,
            "visibility": "public",
        }
        return self._request("POST", "/admin/users", json=payload)

    def get_user(self, username: str) -> dict[str, Any]:
        return self._request("GET", f"/users/{username}")

    def ensure_user(self, username: str, email: str, password: str) -> dict[str, Any]:
        try:
            return self.get_user(username)
        except GiteaAPIError as exc:
            if exc.status_code == 404:
                return self.create_user(username, email, password)
            raise

    def create_org_repo(
        self,
        org: str,
        name: str,
        description: str = "",
        private: bool = False,
        auto_init: bool = True,
    ) -> dict[str, Any]:
        payload = {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": auto_init,
            "default_branch": "main",
        }
        return self._request("POST", f"/orgs/{org}/repos", json=payload)

    def get_repo(self, owner: str, name: str) -> dict[str, Any]:
        return self._request("GET", f"/repos/{owner}/{name}")

    def ensure_org_repo(
        self,
        org: str,
        name: str,
        description: str = "",
        private: bool = False,
    ) -> dict[str, Any]:
        self.ensure_organization(org)
        try:
            return self.get_repo(org, name)
        except GiteaAPIError as exc:
            if exc.status_code == 404:
                return self.create_org_repo(
                    org=org,
                    name=name,
                    description=description,
                    private=private,
                )
            raise

    def create_repo_webhook(
        self,
        owner: str,
        repo: str,
        target_url: str,
        secret: str = "",
    ) -> dict[str, Any]:
        payload = {
            "type": "gitea",
            "config": {
                "url": target_url,
                "content_type": "json",
                "secret": secret,
            },
            "events": ["push", "release"],
            "active": True,
        }
        return self._request("POST", f"/repos/{owner}/{repo}/hooks", json=payload)
