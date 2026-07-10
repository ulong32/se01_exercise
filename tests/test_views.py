import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.events.models import Event, Category

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="password")

@pytest.fixture
def category():
    return Category.objects.create(name="Conference")

@pytest.fixture
def event(user, category):
    return Event.objects.create(
        title="Test Event",
        description="Test Description",
        date=timezone.now(),
        location="Test Location",
        category=category,
        creator=user
    )

@pytest.mark.django_db
def test_home_view(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome" in response.content

@pytest.mark.django_db
def test_event_list_view_empty(client):
    response = client.get(reverse("events:event_list"))
    assert response.status_code == 200
    assert b"No events available" in response.content

@pytest.mark.django_db
def test_event_list_view_with_events(client, event):
    response = client.get(reverse("events:event_list"))
    assert response.status_code == 200
    assert event.title.encode() in response.content

@pytest.mark.django_db
def test_event_detail_view_success(client, event):
    response = client.get(reverse("events:event_detail", args=[event.id]))
    assert response.status_code == 200
    assert event.title.encode() in response.content

@pytest.mark.django_db
def test_event_detail_view_404(client):
    response = client.get(reverse("events:event_detail", args=[999]))
    assert response.status_code == 404

@pytest.mark.django_db
def test_event_create_view_get(client):
    response = client.get(reverse("events:event_create"))
    assert response.status_code == 200
    assert b"Create Event" in response.content

@pytest.mark.django_db
def test_event_create_view_post_success(client, category):
    # Ensure there is a user to act as creator
    user = User.objects.create_user(username="default_creator", password="password")
    client.force_login(user)
    
    data = {
        "title": "New Event",
        "description": "New Description",
        "date": timezone.now().isoformat(),
        "location": "New Location",
        "category_id": category.id
    }
    response = client.post(reverse("events:event_create"), data)
    assert response.status_code == 302
    assert Event.objects.count() == 1
    assert Event.objects.first().title == "New Event"

@pytest.mark.django_db
def test_event_create_view_post_missing_fields(client):
    response = client.post(reverse("events:event_create"), {})
    assert response.status_code == 400
