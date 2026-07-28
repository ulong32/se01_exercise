## Why

The application currently only has `users` and `events` tables with no way for users to bookmark or save events for future reference. The README lists a `favorites` junction table as an unimplemented feature. Implementing "Saved Events" adds meaningful user engagement — authenticated users can build a personal collection of events they're interested in, making the platform more useful as the event catalogue grows.

## What Changes

- Add an explicit `Favorite` junction model (`apps/events/models.py`) linking `User` ↔ `Event` with a `created_at` timestamp and a `unique_together` constraint to prevent duplicates.
- Add service functions in `services.py`: `toggle_favorite(user, event) -> bool` for toggling, returning the new favorited state.
- Add selector functions in `selectors.py`: `get_user_favorites(user) -> QuerySet[Event]` and `is_favorited(user, event) -> bool`.
- Add a toggle endpoint `POST /events/<event_id>/favorite/` (login required) returning an HTMX partial for the button state.
- Add a saved events listing page at `GET /events/saved/` (login required) showing all favorited events.
- Add favorite/unfavorite button (heart icon) to event cards in `_event_results.html` and the detail view in `event_detail.html`, using HTMX for seamless toggling.
- Register `Favorite` model in Django admin.
- Add unit tests for toggle behavior, permission checks, and saved events retrieval.

## Capabilities

### New Capabilities
- `saved-events`: Covers the Favorite junction model, toggle service logic, saved events listing view, HTMX-driven favorite button UI, and associated endpoints.

### Modified Capabilities
- `database-schema`: Adding the Favorite junction model to the database schema specification.
- `basic-views`: Adding the saved events listing view and favorite toggle endpoint to the views specification.

## Impact

- **Models**: New `Favorite` model in `apps/events/models.py` — requires a new migration.
- **Admin**: `apps/events/admin.py` updated with `FavoriteAdmin` registration.
- **Services/Selectors**: New functions in `services.py` and `selectors.py`.
- **Views/URLs**: Two new view functions and URL patterns in `apps/events/views.py` and `urls.py`.
- **Templates**: `_event_results.html`, `event_detail.html` modified; new `_favorite_button.html` partial and `event_saved.html` page.
- **Static assets**: Minor CSS additions for favorite button styling.
- **Tests**: New test cases in `apps/events/tests.py`.
