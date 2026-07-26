## MODIFIED Requirements

### Requirement: Event List View
The system SHALL provide an event list view that returns all events in the database. The template SHALL display events using semantic HTML (`<article>` or structured list items) with CSS classes for layout. The view SHALL detect HTMX requests via the `HX-Request` header and return only the event results partial template for HTMX requests, while returning the full page template for normal requests. The search input SHALL include HTMX attributes (`hx-get`, `hx-trigger`, `hx-target`) to enable dynamic partial-page updates.

#### Scenario: Viewing the event list with events present
- **WHEN** user sends a GET request to `/events/`
- **THEN** the system returns an HTTP 200 response containing a list of all events rendered with semantic HTML elements and CSS classes

#### Scenario: Viewing the event list with no events
- **WHEN** user sends a GET request to `/events/` and no events exist
- **THEN** the system returns an HTTP 200 response indicating that no events are available

#### Scenario: HTMX search request returns partial HTML
- **WHEN** user sends a GET request to `/events/` with the `HX-Request: true` header and a `q` query parameter
- **THEN** the system returns an HTTP 200 response containing only the event results HTML fragment matching the search query
