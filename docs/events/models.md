# Event Models

This file defines the database schema for the events application.

## Models

### `Category`
Represents an event category.
- `name`: `CharField(max_length=100)`

### `Event`
Represents a local event.
- `title`: `CharField(max_length=200)`
- `description`: `TextField()`
- `date`: `DateTimeField()`
- `location`: `CharField(max_length=255)`
- `category`: `ForeignKey(Category)`
- `creator`: `ForeignKey(User)` - The user who created the event.
- `created_at`: `DateTimeField(auto_now_add=True)`

### `Favorite`
Junction table mapping users to their saved/favorited events.
- `user`: `ForeignKey(User)`
- `event`: `ForeignKey(Event)`
- `created_at`: `DateTimeField(auto_now_add=True)`
- **Constraints**: `unique_together = ("user", "event")` to prevent duplicate favorites.
