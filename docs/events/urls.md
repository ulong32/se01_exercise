# Event URLs

This file maps URL patterns to view functions for the events application.

## URL Patterns

- `""` (name: `event_list`): Maps to `views.event_list` - Displays all events.
- `"saved/"` (name: `event_saved`): Maps to `views.event_saved` - Displays the user's favorited events.
- `"<int:event_id>/"` (name: `event_detail`): Maps to `views.event_detail` - Displays details for a specific event.
- `"<int:event_id>/favorite/"` (name: `event_toggle_favorite`): Maps to `views.event_toggle_favorite` - Toggles the favorite status for an event.
- `"create/"` (name: `event_create`): Maps to `views.event_create` - Form for creating a new event.
- `"<int:event_id>/edit/"` (name: `event_edit`): Maps to `views.event_edit` - Form for editing an event.
- `"<int:event_id>/delete/"` (name: `event_delete`): Maps to `views.event_delete` - Endpoint to delete an event.
