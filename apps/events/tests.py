from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.utils import timezone

from apps.events.models import Category, Event, Favorite
from apps.events.selectors import (
    get_events,
    get_favorited_event_ids,
    get_user_favorites,
)
from apps.events.services import toggle_favorite

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
        date=timezone.now() + timedelta(days=1),
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


@pytest.fixture
def second_category():
    return Category.objects.create(name="Meetup")


@pytest.fixture
def multiple_events(creator, category, second_category):
    now = timezone.now()
    e1 = Event.objects.create(
        title="Django Workshop",
        description="Learn Django basics",
        date=now + timedelta(days=1),
        location="Tokyo Shibuya",
        category=category,
        creator=creator,
    )
    e2 = Event.objects.create(
        title="Python Meetup",
        description="Casual meetup",
        date=now + timedelta(days=5),
        location="Osaka Umeda",
        category=second_category,
        creator=creator,
    )
    e3 = Event.objects.create(
        title="Advanced Django",
        description="Deep dive",
        date=now + timedelta(days=10),
        location="Tokyo Shinjuku",
        category=category,
        creator=creator,
    )
    return [e1, e2, e3], now


@pytest.mark.django_db
def test_get_events_no_filter(multiple_events):
    events, _ = multiple_events
    assert get_events().count() == 3


@pytest.mark.django_db
def test_get_events_filter_query(multiple_events):
    events, _ = multiple_events
    res = get_events(query="Workshop")
    assert res.count() == 1
    assert res.first().title == "Django Workshop"


@pytest.mark.django_db
def test_get_events_filter_category(multiple_events, second_category):
    events, _ = multiple_events
    res = get_events(category_id=second_category.id)
    assert res.count() == 1
    assert res.first().title == "Python Meetup"


@pytest.mark.django_db
def test_get_events_filter_date_range(multiple_events):
    events, now = multiple_events
    res = get_events(
        date_from=(now + timedelta(days=4)).date(),
        date_to=(now + timedelta(days=6)).date(),
    )
    assert res.count() == 1
    assert res.first().title == "Python Meetup"


@pytest.mark.django_db
def test_get_events_filter_location(multiple_events):
    events, _ = multiple_events
    res = get_events(location="Tokyo")
    assert res.count() == 2


@pytest.mark.django_db
def test_get_events_combined(multiple_events, category):
    events, _ = multiple_events
    res = get_events(query="Django", location="Shinjuku", category_id=category.id)
    assert res.count() == 1
    assert res.first().title == "Advanced Django"


@pytest.mark.django_db
def test_event_list_view_filters(client, multiple_events, second_category):
    response = client.get(
        reverse("events:event_list"), {"q": "Meetup", "location": "Osaka"}
    )
    assert response.status_code == 200
    assert b"Python Meetup" in response.content
    assert b"Django Workshop" not in response.content
    assert response.context["q"] == "Meetup"
    assert response.context["location"] == "Osaka"


@pytest.mark.django_db
def test_event_list_view_invalid_params(client, multiple_events):
    response = client.get(
        reverse("events:event_list"), {"category": "invalid", "date_from": "not-a-date"}
    )
    assert response.status_code == 200
    assert len(response.context["events"]) == 3


@pytest.mark.django_db
def test_event_list_view_htmx_partial(client, multiple_events):
    response = client.get(
        reverse("events:event_list"),
        {"location": "Tokyo"},
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == 200
    assert b"event-list" in response.content
    assert b"<html" not in response.content
    assert b"Django Workshop" in response.content
    assert b"Python Meetup" not in response.content


@pytest.fixture
def past_event(creator, category):
    return Event.objects.create(
        title="Past Event Title",
        description="Happened yesterday",
        date=timezone.now() - timedelta(days=1),
        location="Old Location",
        category=category,
        creator=creator,
    )


@pytest.fixture
def many_events(creator, category):
    events = []
    now = timezone.now()
    for i in range(15):
        events.append(
            Event.objects.create(
                title=f"Paginated Event {i:02d}",
                description="Test pagination",
                date=now + timedelta(days=i + 1),
                location="Tokyo",
                category=category,
                creator=creator,
            )
        )
    return events


@pytest.mark.django_db
def test_get_events_exclude_past(event, past_event):
    res_default = get_events()
    assert event in res_default
    assert past_event not in res_default

    res_false = get_events(include_past=False)
    assert event in res_false
    assert past_event not in res_false


@pytest.mark.django_db
def test_get_events_include_past(event, past_event):
    res_true = get_events(include_past=True)
    assert event in res_true
    assert past_event in res_true


@pytest.mark.django_db
def test_event_list_exclude_and_include_past(client, event, past_event):
    res_default = client.get(reverse("events:event_list"))
    assert res_default.status_code == 200
    assert b"Original Event" in res_default.content
    assert b"Past Event Title" not in res_default.content

    res_include = client.get(reverse("events:event_list"), {"include_past": "true"})
    assert res_include.status_code == 200
    assert b"Original Event" in res_include.content
    assert b"Past Event Title" in res_include.content
    assert b"past-event" in res_include.content


@pytest.mark.django_db
def test_pagination_pages(client, many_events):
    res_page1 = client.get(reverse("events:event_list"))
    assert res_page1.status_code == 200
    assert len(res_page1.context["page_obj"]) == 12
    assert res_page1.context["page_obj"].number == 1
    assert b"Paginated Event 00" in res_page1.content
    assert b"Paginated Event 11" in res_page1.content
    assert b"Paginated Event 12" not in res_page1.content

    res_page2 = client.get(reverse("events:event_list"), {"page": "2"})
    assert res_page2.status_code == 200
    assert len(res_page2.context["page_obj"]) == 3
    assert res_page2.context["page_obj"].number == 2
    assert b"Paginated Event 12" in res_page2.content
    assert b"Paginated Event 14" in res_page2.content
    assert b"Paginated Event 00" not in res_page2.content


@pytest.mark.django_db
def test_pagination_invalid_page(client, many_events):
    for invalid_page in ["999", "abc", "-1"]:
        res = client.get(reverse("events:event_list"), {"page": invalid_page})
        assert res.status_code == 200
        assert res.context["page_obj"].number == 1
        assert len(res.context["page_obj"]) == 12


@pytest.mark.django_db
def test_pagination_with_filters(client, many_events, second_category, creator):
    now = timezone.now()
    Event.objects.create(
        title="Other Category Event 01",
        description="Different category",
        date=now + timedelta(days=2),
        location="Tokyo",
        category=second_category,
        creator=creator,
    )
    res = client.get(
        reverse("events:event_list"),
        {"category": many_events[0].category.id, "page": "2"},
    )
    assert res.status_code == 200
    assert len(res.context["page_obj"]) == 3
    for ev in res.context["page_obj"]:
        assert ev.category == many_events[0].category


@pytest.mark.django_db
def test_pagination_htmx(client, many_events):
    res = client.get(
        reverse("events:event_list"),
        {"page": "2"},
        HTTP_HX_REQUEST="true",
    )
    assert res.status_code == 200
    assert b"event-results" in res.content
    assert b"<html" not in res.content
    assert b"Paginated Event 12" in res.content
    assert b"pagination" in res.content
    assert b"&laquo; Previous" in res.content


@pytest.mark.django_db
def test_toggle_favorite_service(creator, event):
    assert toggle_favorite(creator, event) is True
    assert Favorite.objects.filter(user=creator, event=event).exists()
    assert toggle_favorite(creator, event) is False
    assert not Favorite.objects.filter(user=creator, event=event).exists()


@pytest.mark.django_db
def test_get_user_favorites_selector(creator, event, category):
    event2 = Event.objects.create(
        title="Second Event",
        description="Second Description",
        date=timezone.now() + timedelta(days=2),
        location="Location 2",
        category=category,
        creator=creator,
    )
    toggle_favorite(creator, event)
    toggle_favorite(creator, event2)
    favs = list(get_user_favorites(creator))
    assert len(favs) == 2
    assert favs[0] == event2
    assert favs[1] == event


@pytest.mark.django_db
def test_get_favorited_event_ids_selector(creator, event):
    assert get_favorited_event_ids(creator) == set()
    toggle_favorite(creator, event)
    assert get_favorited_event_ids(creator) == {event.id}
    assert get_favorited_event_ids(AnonymousUser()) == set()


@pytest.mark.django_db
def test_toggle_favorite_endpoint(client, creator, event):
    url = reverse("events:event_toggle_favorite", args=[event.id])
    res_unauth = client.post(url)
    assert res_unauth.status_code == 302
    assert "/users/login/" in res_unauth.url

    client.force_login(creator)
    res_get = client.get(url)
    assert res_get.status_code == 405

    res_post1 = client.post(url)
    assert res_post1.status_code == 200
    assert Favorite.objects.filter(user=creator, event=event).exists()
    assert b"is-favorited" in res_post1.content

    res_post2 = client.post(url)
    assert res_post2.status_code == 200
    assert not Favorite.objects.filter(user=creator, event=event).exists()


@pytest.mark.django_db
def test_event_saved_view(client, creator, event):
    url = reverse("events:event_saved")
    res_unauth = client.get(url)
    assert res_unauth.status_code == 302

    client.force_login(creator)
    res_empty = client.get(url)
    assert res_empty.status_code == 200
    assert b"You have no saved events yet." in res_empty.content

    toggle_favorite(creator, event)
    res_saved = client.get(url)
    assert res_saved.status_code == 200
    assert event.title.encode() in res_saved.content


@pytest.mark.django_db
def test_event_list_context_favorited_ids(client, creator, event):
    url = reverse("events:event_list")
    res_unauth = client.get(url)
    assert res_unauth.status_code == 200
    assert res_unauth.context["favorited_ids"] == set()

    client.force_login(creator)
    toggle_favorite(creator, event)
    res_auth = client.get(url)
    assert res_auth.status_code == 200
    assert res_auth.context["favorited_ids"] == {event.id}


@pytest.mark.django_db
def test_event_detail_context_is_favorited(client, creator, event):
    url = reverse("events:event_detail", args=[event.id])
    res_unauth = client.get(url)
    assert res_unauth.status_code == 200
    assert res_unauth.context["is_favorited"] is False

    client.force_login(creator)
    res_auth1 = client.get(url)
    assert res_auth1.status_code == 200
    assert res_auth1.context["is_favorited"] is False

    toggle_favorite(creator, event)
    res_auth2 = client.get(url)
    assert res_auth2.status_code == 200
    assert res_auth2.context["is_favorited"] is True


@pytest.mark.django_db
def test_create_event_deduplication_within_window(creator, category):
    from apps.events.services import create_event
    now = timezone.now()
    event1 = create_event(
        title="Dedup Event",
        description="Description 1",
        date=now + timedelta(days=1),
        location="Location 1",
        category=category,
        creator=creator,
    )
    event2 = create_event(
        title="Dedup Event",
        description="Description 2",
        date=now + timedelta(days=1),
        location="Location 2",
        category=category,
        creator=creator,
    )
    assert event1.id == event2.id
    assert Event.objects.filter(title="Dedup Event").count() == 1


@pytest.mark.django_db
def test_create_event_no_dedup_outside_window_or_diff_user(creator, other_user, category):
    from unittest.mock import patch
    from apps.events.services import create_event
    now = timezone.now()
    event1 = create_event(
        title="Dedup Event 2",
        description="Description 1",
        date=now + timedelta(days=1),
        location="Location 1",
        category=category,
        creator=creator,
    )
    event_other = create_event(
        title="Dedup Event 2",
        description="Description Other",
        date=now + timedelta(days=1),
        location="Location Other",
        category=category,
        creator=other_user,
    )
    assert event1.id != event_other.id
    assert Event.objects.filter(title="Dedup Event 2").count() == 2

    with patch("django.utils.timezone.now", return_value=now + timedelta(seconds=6)):
        event_after = create_event(
            title="Dedup Event 2",
            description="Description After",
            date=now + timedelta(days=1),
            location="Location After",
            category=category,
            creator=creator,
        )
        assert event1.id != event_after.id
        assert Event.objects.filter(title="Dedup Event 2").count() == 3
