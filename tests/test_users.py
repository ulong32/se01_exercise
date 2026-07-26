import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
def test_register_get(client):
    response = client.get(reverse("users:register"))
    assert response.status_code == 200
    assert b"Register User" in response.content


@pytest.mark.django_db
def test_register_post_success(client):
    response = client.post(
        reverse("users:register"), {"username": "newuser", "password": "password123"}
    )
    assert response.status_code == 302
    assert User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_register_csrf_enforced():
    from django.test import Client

    csrf_client = Client(enforce_csrf_checks=True)
    response = csrf_client.post(
        reverse("users:register"), {"username": "csrf_test", "password": "password123"}
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_login_get(client):
    response = client.get(reverse("users:login"))
    assert response.status_code == 200
    assert b"Login" in response.content


@pytest.mark.django_db
def test_login_post_success(client):
    User.objects.create_user(username="testlogin", password="password123")
    response = client.post(
        reverse("users:login"), {"username": "testlogin", "password": "password123"}
    )
    assert response.status_code == 302
    assert "_auth_user_id" in client.session


@pytest.mark.django_db
def test_logout(client):
    user = User.objects.create_user(username="testlogout", password="password123")
    client.force_login(user)
    response = client.post(reverse("users:logout"))
    assert response.status_code == 302
    assert "_auth_user_id" not in client.session
