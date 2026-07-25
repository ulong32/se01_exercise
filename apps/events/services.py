from .models import Event

def create_event(title: str, description: str, date, location: str, category, creator) -> Event:
    """Creates a new Event record."""
    return Event.objects.create(
        title=title,
        description=description,
        date=date,
        location=location,
        category=category,
        creator=creator
    )
