import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Idempotently create or verify an administrative superuser account."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            default=os.environ.get("ADMIN_USERNAME", "admin"),
            help="Username for the superuser (default: env ADMIN_USERNAME or 'admin')",
        )
        parser.add_argument(
            "--email",
            default=os.environ.get("ADMIN_EMAIL", "admin@example.com"),
            help="Email for the superuser (default: env ADMIN_EMAIL or 'admin@example.com')",
        )
        parser.add_argument(
            "--password",
            default=os.environ.get("ADMIN_PASSWORD", "adminpassword"),
            help="Password for the superuser (default: env ADMIN_PASSWORD or 'adminpassword')",
        )

    def handle(self, *args, **options):
        User = get_user_model()
        username = options["username"]
        email = options["email"]
        password = options["password"]

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.SUCCESS(f"Superuser '{username}' already exists.")
            )
        else:
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created superuser '{username}' with email '{email}'."
                )
            )
