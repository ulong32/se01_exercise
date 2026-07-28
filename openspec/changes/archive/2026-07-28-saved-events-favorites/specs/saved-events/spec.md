## ADDED Requirements

### Requirement: Favorite Model Definition
The system SHALL define a `Favorite` model in `apps/events/models.py` representing a many-to-many relationship between users and events. The model SHALL contain a `user` foreign key to `settings.AUTH_USER_MODEL` (on_delete=CASCADE), an `event` foreign key to `Event` (on_delete=CASCADE), and a `created_at` DateTimeField with `auto_now_add=True`. The model SHALL enforce a unique constraint on `(user, event)` to prevent duplicate favorites. The model SHALL implement a `__str__` method returning a human-readable representation.

#### Scenario: Creating a favorite
- **WHEN** a valid user and event are provided
- **THEN** a Favorite record is created in the database with an auto-populated `created_at` timestamp

#### Scenario: Preventing duplicate favorites
- **WHEN** a user attempts to favorite the same event twice
- **THEN** the system raises an IntegrityError due to the unique constraint on `(user, event)`

#### Scenario: Cascade deletion from user
- **WHEN** a user is deleted from the system
- **THEN** all Favorite records for that user are automatically deleted

#### Scenario: Cascade deletion from event
- **WHEN** an event is deleted from the system
- **THEN** all Favorite records for that event are automatically deleted

### Requirement: Toggle Favorite Service
The system SHALL provide a service function `toggle_favorite(user, event) -> bool` in `apps/events/services.py`. When the user has NOT favorited the event, the function SHALL create a Favorite record and return `True`. When the user HAS already favorited the event, the function SHALL delete the Favorite record and return `False`.

#### Scenario: Favoriting an event for the first time
- **WHEN** `toggle_favorite(user, event)` is called and no Favorite exists for the pair
- **THEN** a Favorite record is created and the function returns `True`

#### Scenario: Unfavoriting a previously favorited event
- **WHEN** `toggle_favorite(user, event)` is called and a Favorite already exists for the pair
- **THEN** the Favorite record is deleted and the function returns `False`

### Requirement: Favorite Query Selectors
The system SHALL provide selector functions in `apps/events/selectors.py`:
- `get_user_favorites(user) -> QuerySet[Event]`: Returns a QuerySet of Event objects favorited by the given user, ordered by the Favorite's `created_at` descending (most recently saved first).
- `get_favorited_event_ids(user) -> set[int]`: Returns a set of event IDs favorited by the given user, for efficient template-level lookups.

#### Scenario: Retrieving favorites for a user with saved events
- **WHEN** `get_user_favorites(user)` is called for a user who has favorited 3 events
- **THEN** a QuerySet of those 3 Event objects is returned, ordered by most recently favorited first

#### Scenario: Retrieving favorites for a user with no saved events
- **WHEN** `get_user_favorites(user)` is called for a user who has no favorites
- **THEN** an empty QuerySet is returned

#### Scenario: Getting favorited event IDs for template lookup
- **WHEN** `get_favorited_event_ids(user)` is called for a user who has favorited events with IDs 5, 12, 23
- **THEN** the set `{5, 12, 23}` is returned

#### Scenario: Getting favorited event IDs for anonymous user
- **WHEN** `get_favorited_event_ids(user)` is called with an anonymous (unauthenticated) user
- **THEN** an empty set is returned

### Requirement: Toggle Favorite Endpoint
The system SHALL provide an endpoint at `POST /events/<event_id>/favorite/` that toggles the favorite status for the authenticated user and the specified event. The endpoint SHALL be restricted to authenticated users via `@login_required`. The endpoint SHALL call the `toggle_favorite` service function and return the `_favorite_button.html` partial template reflecting the new state. The endpoint SHALL only accept POST requests.

#### Scenario: Authenticated user favorites an event via HTMX
- **WHEN** an authenticated user sends a POST request to `/events/5/favorite/` with `HX-Request: true` header
- **THEN** the system creates a Favorite record and returns an HTTP 200 response containing the favorite button HTML with the "favorited" state

#### Scenario: Authenticated user unfavorites an event via HTMX
- **WHEN** an authenticated user sends a POST request to `/events/5/favorite/` for an already-favorited event with `HX-Request: true` header
- **THEN** the system deletes the Favorite record and returns an HTTP 200 response containing the favorite button HTML with the "not favorited" state

#### Scenario: Unauthenticated user attempts to toggle favorite
- **WHEN** an unauthenticated user sends a POST request to `/events/5/favorite/`
- **THEN** the system redirects to the login page

#### Scenario: Non-POST request to toggle endpoint
- **WHEN** a GET request is sent to `/events/5/favorite/`
- **THEN** the system returns an HTTP 405 Method Not Allowed response

### Requirement: Saved Events Listing Page
The system SHALL provide a view at `GET /events/saved/` that displays all events favorited by the authenticated user. The view SHALL be restricted to authenticated users via `@login_required`. The view SHALL use the `get_user_favorites` selector to retrieve the events and render them using a template that reuses the event card pattern.

#### Scenario: Viewing saved events with favorites present
- **WHEN** an authenticated user with 5 favorited events sends a GET request to `/events/saved/`
- **THEN** the system returns an HTTP 200 response displaying all 5 favorited events

#### Scenario: Viewing saved events with no favorites
- **WHEN** an authenticated user with no favorites sends a GET request to `/events/saved/`
- **THEN** the system returns an HTTP 200 response with an empty-state message indicating no saved events

#### Scenario: Unauthenticated user attempts to view saved events
- **WHEN** an unauthenticated user sends a GET request to `/events/saved/`
- **THEN** the system redirects to the login page

### Requirement: Favorite Button UI Component
The system SHALL render a favorite toggle button as a partial template `_favorite_button.html`. The button SHALL display a filled heart icon (♥) when the event is favorited and an outlined heart icon (♡) when not favorited. The button SHALL use `hx-post` pointing to the toggle endpoint, `hx-swap="outerHTML"` to replace itself with the server response, and include the CSRF token via `hx-headers`. The button SHALL only be rendered for authenticated users.

#### Scenario: Rendering favorite button for unfavorited event
- **WHEN** the template renders the favorite button for an event that the user has NOT favorited
- **THEN** the button displays an outlined heart icon (♡) and has the CSS class `favorite-btn`

#### Scenario: Rendering favorite button for favorited event
- **WHEN** the template renders the favorite button for an event that the user HAS favorited
- **THEN** the button displays a filled heart icon (♥) and has the CSS classes `favorite-btn` and `is-favorited`

#### Scenario: Favorite button not shown for anonymous users
- **WHEN** the template renders an event card for an unauthenticated user
- **THEN** no favorite button is rendered

### Requirement: Favorite Button in Event Cards
The system SHALL include the `_favorite_button.html` partial in the event card template (`_event_results.html`) for each event. The button SHALL be positioned within the event card and SHALL use the `favorited_ids` set from the template context to determine the initial state.

#### Scenario: Event card shows favorite button for authenticated user
- **WHEN** an authenticated user views the event list
- **THEN** each event card includes a favorite toggle button reflecting the current favorite state

#### Scenario: Event card hides favorite button for anonymous user
- **WHEN** an anonymous user views the event list
- **THEN** event cards do not include a favorite button

### Requirement: Favorite Button in Event Detail
The system SHALL include the `_favorite_button.html` partial in the event detail template (`event_detail.html`). The detail page SHALL pass the favorite state of the current event for the authenticated user.

#### Scenario: Event detail shows favorite button for authenticated user
- **WHEN** an authenticated user views the event detail page
- **THEN** the page includes a favorite toggle button reflecting the current favorite state

#### Scenario: Event detail hides favorite button for anonymous user
- **WHEN** an anonymous user views the event detail page
- **THEN** the page does not include a favorite button

### Requirement: Favorite Model Admin Registration
The system SHALL register the `Favorite` model with Django admin. The admin SHALL display `user`, `event`, and `created_at` in the list view, support searching by user username and event title, and use raw_id_fields for `user` and `event`.

#### Scenario: Admin views favorite records
- **WHEN** an admin navigates to the Favorite admin list view
- **THEN** the system displays a table with user, event, and created_at columns

### Requirement: Efficient Favorite State Loading
The system SHALL load the authenticated user's favorited event IDs in the event list view and pass them as a `favorited_ids` set in the template context. This avoids N+1 queries when rendering favorite buttons for multiple event cards.

#### Scenario: Event list view passes favorited IDs
- **WHEN** an authenticated user accesses the event list
- **THEN** the template context includes a `favorited_ids` set containing the IDs of all events the user has favorited

#### Scenario: Event list view for anonymous user
- **WHEN** an anonymous user accesses the event list
- **THEN** the template context includes an empty `favorited_ids` set

### Requirement: Navigation Link to Saved Events
The system SHALL include a "Saved Events" navigation link in the site navigation for authenticated users, linking to `/events/saved/`.

#### Scenario: Authenticated user sees Saved Events link
- **WHEN** an authenticated user views any page
- **THEN** the navigation includes a "Saved Events" link

#### Scenario: Anonymous user does not see Saved Events link
- **WHEN** an anonymous user views any page
- **THEN** the navigation does not include a "Saved Events" link
