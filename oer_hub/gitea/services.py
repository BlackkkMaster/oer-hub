import os
from typing import Optional

from gitea.client import GiteaClient


def get_gitea_client() -> GiteaClient:
    return GiteaClient()


def sync_user_account(user, password: Optional[str] = None):
    client = get_gitea_client()
    git_username = user.username.lower().replace("@", "_").replace(".", "_")
    user_pass = password or os.getenv("GITEA_DEFAULT_USER_PASSWORD", "OerUserSecret2026!")
    client.ensure_user(username=git_username, email=user.email, password=user_pass)

    profile = getattr(user, "profile", None)
    if profile and not profile.git_username:
        profile.git_username = git_username
        profile.save(update_fields=["git_username"])
    return git_username


def sync_course_repository(course):
    client = get_gitea_client()
    org_name = os.getenv("GITEA_ORG_NAME", "department-oer")
    repo_data = client.ensure_org_repo(
        org=org_name,
        name=course.slug,
        description=course.description or course.name,
    )

    clone_url = repo_data.get("clone_url") or f"{client.base_url}/{org_name}/{course.slug}.git"
    html_url = repo_data.get("html_url") or f"{client.base_url}/{org_name}/{course.slug}"

    course.git_repository_url = html_url
    course.git_clone_url = clone_url
    course.save(update_fields=["git_repository_url", "git_clone_url"])
    return repo_data
