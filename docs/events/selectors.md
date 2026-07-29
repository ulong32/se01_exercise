# Event Selectors

This file contains reusable read/query logic for retrieving events from the database.

## Functions

### `get_events`
- **Arguments**: `query` (optional), `category_id` (optional), `date_from` (optional), `date_to` (optional), `location` (optional), `include_past` (default `False`)
- **Returns**: `QuerySet[Event]`
- **Description**: Retrieves a filtered list of Event objects based on various criteria. By default, it filters out past events unless `include_past` is set to `True`.

### `get_user_favorites`
- **Arguments**: `user`
- **Returns**: `QuerySet[Event]`
- **Description**: Retrieves a list of events favorited by the provided user, ordered by the most recently favorited first. Returns an empty QuerySet if the user is not authenticated.

### `get_favorited_event_ids`
- **Arguments**: `user`
- **Returns**: `set[int]`
- **Description**: Retrieves a set of event IDs that the user has favorited. This is useful for efficiently checking favorite status in views and templates. Returns an empty set if the user is not authenticated.
