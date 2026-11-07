import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from users.models import Role

User = get_user_model()


class Command(BaseCommand):
    help = "Initialize superuser from environment variables"

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "adminpassword123")

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            profile = getattr(user, "profile", None)
            if profile:
                profile.role = Role.ADMIN
                profile.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Superuser '{username}' initialized successfully"
                )
            )
        else:
            self.stdout.write(
                self.style.NOTICE(f"Superuser '{username}' already exists")
            )
