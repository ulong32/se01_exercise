from datetime import date

from django.db.models import QuerySet

from .models import Event


def get_events(
    *,
    query: str | None = None,
    category_id: int | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    location: str | None = None,
) -> QuerySet[Event]:
    """Retrieves a filtered QuerySet of Event objects based on criteria."""
    events = Event.objects.all()

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
