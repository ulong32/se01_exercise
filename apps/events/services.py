from datetime import timedelta
from django.utils import timezone
from .models import Event, Favorite


def create_event(
    title: str, description: str, date, location: str, category, creator
) -> Event:
    """Creates a new Event record, with time-window deduplication."""
    time_threshold = timezone.now() - timedelta(seconds=5)
    existing = Event.objects.filter(
        title=title,
        creator=creator,
        date=date,
        created_at__gte=time_threshold,
    ).first()
    if existing:
        return existing

    return Event.objects.create(
        title=title,
        description=description,
        date=date,
        location=location,
        category=category,
        creator=creator,
    )


def update_event(event: Event, **kwargs) -> Event:
    """Updates an existing Event record with provided keyword arguments."""
    for key, value in kwargs.items():
        if hasattr(event, key):
            setattr(event, key, value)
    event.save()
    return event


def delete_event(event: Event) -> None:
    """Deletes an Event record from the database."""
    event.delete()


def toggle_favorite(user, event: Event) -> bool:
    """Toggles favorite status for a user and event.
    Returns True if favorited, False if unfavorited.
    """
    favorite, created = Favorite.objects.get_or_create(user=user, event=event)
    if not created:
        favorite.delete()
        return False
    return True
