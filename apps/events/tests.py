import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from apps.events.models import Category, Event

User = get_user_model()


@pytest.fixture
def creator():
    return User.objects.create_user(username="creator_user", password="password")


@pytest.fixture
def other_user():
    return User.objects.create_user(username="other_user", password="password")


@pytest.fixture
def admin_user():
    return User.objects.create_superuser(
        username="admin_user", password="password", email="admin@example.com"
    )


@pytest.fixture
def category():
    return Category.objects.create(name="Workshop")


@pytest.fixture
def event(creator, category):
    return Event.objects.create(
        title="Original Event",
        description="Original Description",
        date=timezone.now(),
        location="Original Location",
        category=category,
        creator=creator,
    )


@pytest.mark.django_db
def test_event_edit_get_authorized_creator(client, event, creator):
    client.force_login(creator)
    response = client.get(reverse("events:event_edit", args=[event.id]))
    assert response.status_code == 200
    assert b"Edit Event" in response.content
    assert event.title.encode() in response.content


@pytest.mark.django_db
def test_event_edit_post_success_creator(client, event, creator, category):
    client.force_login(creator)
    data = {
        "title": "Updated Event Title",
        "description": "Updated Description",
        "date": timezone.now().isoformat(),
        "location": "Updated Location",
        "category_id": category.id,
    }
    response = client.post(reverse("events:event_edit", args=[event.id]), data)
    assert response.status_code == 302
    event.refresh_from_db()
    assert event.title == "Updated Event Title"
    assert event.location == "Updated Location"


@pytest.mark.django_db
def test_event_edit_post_success_admin(client, event, admin_user, category):
    client.force_login(admin_user)
    data = {
        "title": "Admin Updated Title",
        "description": "Admin Description",
        "date": timezone.now().isoformat(),
        "location": "Admin Location",
        "category_id": category.id,
    }
    response = client.post(reverse("events:event_edit", args=[event.id]), data)
    assert response.status_code == 302
    event.refresh_from_db()
    assert event.title == "Admin Updated Title"


@pytest.mark.django_db
def test_event_delete_post_success_creator(client, event, creator):
    client.force_login(creator)
    response = client.post(reverse("events:event_delete", args=[event.id]))
    assert response.status_code == 302
    assert Event.objects.filter(pk=event.id).count() == 0


@pytest.mark.django_db
def test_event_delete_post_success_admin(client, event, admin_user):
    client.force_login(admin_user)
    response = client.post(reverse("events:event_delete", args=[event.id]))
    assert response.status_code == 302
    assert Event.objects.filter(pk=event.id).count() == 0


@pytest.mark.django_db
def test_event_edit_unauthenticated(client, event):
    response = client.get(reverse("events:event_edit", args=[event.id]))
    assert response.status_code == 302
    assert "users/login" in response.url


@pytest.mark.django_db
def test_event_edit_unauthorized_user(client, event, other_user):
    client.force_login(other_user)
    response = client.get(reverse("events:event_edit", args=[event.id]))
    assert response.status_code == 403
    assert b"permission" in response.content.lower()


@pytest.mark.django_db
def test_event_delete_unauthenticated(client, event):
    response = client.post(reverse("events:event_delete", args=[event.id]))
    assert response.status_code == 302
    assert "users/login" in response.url


@pytest.mark.django_db
def test_event_delete_unauthorized_user(client, event, other_user):
    client.force_login(other_user)
    response = client.post(reverse("events:event_delete", args=[event.id]))
    assert response.status_code == 403
    assert b"permission" in response.content.lower()
