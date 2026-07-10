## ADDED Requirements

### Requirement: Home Page View
The system SHALL provide a home page view at the root URL (`/`) that returns a welcome response.

#### Scenario: Accessing the home page
- **WHEN** user sends a GET request to `/`
- **THEN** the system returns an HTTP 200 response containing a welcome message

### Requirement: Event List View
The system SHALL provide an event list view that returns all events in the database.

#### Scenario: Viewing the event list with events present
- **WHEN** user sends a GET request to `/events/`
- **THEN** the system returns an HTTP 200 response containing a list of all events with their titles, dates, and locations

#### Scenario: Viewing the event list with no events
- **WHEN** user sends a GET request to `/events/` and no events exist
- **THEN** the system returns an HTTP 200 response indicating that no events are available

### Requirement: Event Detail View
The system SHALL provide an event detail view that returns the full details of a single event by its ID.

#### Scenario: Viewing an existing event
- **WHEN** user sends a GET request to `/events/<event_id>/` with a valid event ID
- **THEN** the system returns an HTTP 200 response containing the event's title, description, date, location, category, and creator

#### Scenario: Viewing a non-existent event
- **WHEN** user sends a GET request to `/events/<event_id>/` with an ID that does not exist
- **THEN** the system returns an HTTP 404 response

### Requirement: Event Create Form View
The system SHALL provide a view at `/events/create/` that responds to GET requests with a placeholder for the event creation form.

#### Scenario: Accessing the event creation page
- **WHEN** user sends a GET request to `/events/create/`
- **THEN** the system returns an HTTP 200 response indicating the event creation form

### Requirement: Event Create Handler
The system SHALL provide a handler at `/events/create/` that processes POST requests to create a new event.

#### Scenario: Creating an event with valid data
- **WHEN** user sends a POST request to `/events/create/` with title, description, date, location, and category_id
- **THEN** the system creates a new Event in the database and redirects to the event detail page

#### Scenario: Creating an event with missing required fields
- **WHEN** user sends a POST request to `/events/create/` with missing required fields
- **THEN** the system returns an HTTP 400 response indicating the missing fields

### Requirement: Events URL Routing
The system SHALL define URL patterns in `apps/events/urls.py` and include them in the project-level URL configuration.

#### Scenario: URL namespace resolution
- **WHEN** any event-related URL is accessed
- **THEN** it is routed through the `events` app URL configuration under the `events` namespace
