import pytest
from io import StringIO
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.core.management import call_command
from apps.events.models import Event, Category


@pytest.mark.django_db
def test_setup_admin_command_creates_superuser():
    User = get_user_model()
    out = StringIO()
    call_command(
        "setup_admin",
        username="newadmin",
        email="newadmin@example.com",
        password="password123",
        stdout=out,
    )
    output = out.getvalue()
    assert "Successfully created superuser 'newadmin'" in output
    user = User.objects.get(username="newadmin")
    assert user.is_superuser
    assert user.is_staff
    assert user.email == "newadmin@example.com"


@pytest.mark.django_db
def test_setup_admin_command_idempotent():
    User = get_user_model()
    User.objects.create_superuser(
        username="existingadmin", email="existing@example.com", password="password123"
    )
    out = StringIO()
    call_command(
        "setup_admin",
        username="existingadmin",
        email="existing@example.com",
        password="password123",
        stdout=out,
    )
    output = out.getvalue()
    assert "Superuser 'existingadmin' already exists." in output
    assert User.objects.filter(username="existingadmin").count() == 1


def test_admin_model_registration():
    assert admin.site.is_registered(Event)
    assert admin.site.is_registered(Category)
