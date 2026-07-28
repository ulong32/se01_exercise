## ADDED Requirements

### Requirement: Toggle Favorite Endpoint
The system SHALL provide a view at `POST /events/<event_id>/favorite/` that toggles the authenticated user's favorite status for the specified event. The view SHALL be decorated with `@login_required`. The view SHALL delegate to the `toggle_favorite` service function and return the `_favorite_button.html` partial template. The view SHALL reject non-POST requests with HTTP 405.

#### Scenario: Toggling favorite on via POST
- **WHEN** an authenticated user sends a POST request to `/events/5/favorite/`
- **THEN** the system toggles the favorite status and returns an HTTP 200 response with the updated button partial

#### Scenario: Unauthenticated toggle attempt
- **WHEN** an unauthenticated user sends a POST request to `/events/5/favorite/`
- **THEN** the system redirects to the login page

#### Scenario: Non-POST request rejected
- **WHEN** a GET request is sent to `/events/5/favorite/`
- **THEN** the system returns HTTP 405 Method Not Allowed

### Requirement: Saved Events Listing View
The system SHALL provide a view at `GET /events/saved/` that displays all events favorited by the authenticated user. The view SHALL be restricted to authenticated users via `@login_required`. The view SHALL use the `get_user_favorites` selector and render a template displaying the user's favorited events.

#### Scenario: Viewing saved events with favorites
- **WHEN** an authenticated user with favorited events sends a GET request to `/events/saved/`
- **THEN** the system returns an HTTP 200 response displaying the user's favorited events

#### Scenario: Viewing saved events with no favorites
- **WHEN** an authenticated user with no favorites sends a GET request to `/events/saved/`
- **THEN** the system returns an HTTP 200 response with an empty-state message

#### Scenario: Unauthenticated access to saved events
- **WHEN** an unauthenticated user sends a GET request to `/events/saved/`
- **THEN** the system redirects to the login page

### Requirement: Favorite State in Event List Context
The system SHALL pass a `favorited_ids` set in the template context of the event list view containing the IDs of events favorited by the authenticated user. For anonymous users, the set SHALL be empty.

#### Scenario: Authenticated user event list context
- **WHEN** an authenticated user accesses the event list
- **THEN** the template context includes `favorited_ids` with the user's favorited event IDs

#### Scenario: Anonymous user event list context
- **WHEN** an anonymous user accesses the event list
- **THEN** the template context includes an empty `favorited_ids` set

### Requirement: Favorite State in Event Detail Context
The system SHALL pass an `is_favorited` boolean in the template context of the event detail view indicating whether the authenticated user has favorited the displayed event. For anonymous users, `is_favorited` SHALL be `False`.

#### Scenario: Authenticated user viewing favorited event detail
- **WHEN** an authenticated user who has favorited event 5 accesses `/events/5/`
- **THEN** the template context includes `is_favorited=True`

#### Scenario: Authenticated user viewing non-favorited event detail
- **WHEN** an authenticated user who has NOT favorited event 5 accesses `/events/5/`
- **THEN** the template context includes `is_favorited=False`

#### Scenario: Anonymous user viewing event detail
- **WHEN** an anonymous user accesses `/events/5/`
- **THEN** the template context includes `is_favorited=False`
