from .models import Event


def create_event(
    title: str, description: str, date, location: str, category, creator
) -> Event:
    """Creates a new Event record."""
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
