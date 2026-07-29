# Event Services

This file contains the business workflow logic for events, separating it from views.

## Functions

### `create_event`
- **Arguments**: `title`, `description`, `date`, `location`, `category`, `creator`
- **Returns**: `Event`
- **Description**: Creates a new Event record. It includes time-window deduplication logic, preventing creation of an identical event (same title, creator, and date) within a 5-second window.

### `update_event`
- **Arguments**: `event: Event`, `**kwargs`
- **Returns**: `Event`
- **Description**: Updates an existing Event record with the provided keyword arguments and saves it to the database.

### `delete_event`
- **Arguments**: `event: Event`
- **Returns**: `None`
- **Description**: Deletes the specified Event record from the database.

### `toggle_favorite`
- **Arguments**: `user`, `event: Event`
- **Returns**: `bool` (True if favorited, False if unfavorited)
- **Description**: Toggles the favorite status of an event for a specific user. It handles the creation or deletion of the `Favorite` record appropriately.
