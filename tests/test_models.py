import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.events.models import Category, Event

User = get_user_model()


@pytest.mark.django_db
def test_category_creation_and_str():
    category = Category.objects.create(name="Conference")
    assert category.name == "Conference"
    assert str(category) == "Conference"


@pytest.mark.django_db
def test_event_creation_and_str():
    user = User.objects.create_user(username="testuser", password="password")
    category = Category.objects.create(name="Meetup")
    event = Event.objects.create(
        title="Django Meetup",
        description="A great meetup",
        date=timezone.now(),
        location="Tokyo",
        category=category,
        creator=user,
    )
    assert event.title == "Django Meetup"
    assert event.location == "Tokyo"
    assert event.category == category
    assert event.creator == user
    assert str(event) == "Django Meetup"
