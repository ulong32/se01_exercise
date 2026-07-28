from datetime import date

from django.db.models import QuerySet
from django.utils import timezone

from .models import Event, Favorite


def get_events(
    *,
    query: str | None = None,
    category_id: int | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    location: str | None = None,
    include_past: bool = False,
) -> QuerySet[Event]:
    """Retrieves a filtered QuerySet of Event objects based on criteria."""
    events = Event.objects.all()

    if not include_past:
        events = events.filter(date__gte=timezone.now())

    if query:
        events = events.filter(title__icontains=query)
    if category_id is not None:
        events = events.filter(category_id=category_id)
    if date_from is not None:
        events = events.filter(date__date__gte=date_from)
    if date_to is not None:
        events = events.filter(date__date__lte=date_to)
    if location:
        events = events.filter(location__icontains=location)

    return events


def get_user_favorites(user) -> QuerySet[Event]:
    """Retrieves events favorited by the user, ordered by most recently favorited."""
    if not user.is_authenticated:
        return Event.objects.none()
    return Event.objects.filter(favorites__user=user).order_by("-favorites__created_at")


def get_favorited_event_ids(user) -> set[int]:
    """Retrieves a set of event IDs favorited by the user."""
    if not user.is_authenticated:
        return set()
    return set(Favorite.objects.filter(user=user).values_list("event_id", flat=True))
