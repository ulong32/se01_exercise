## MODIFIED Requirements

### Requirement: Home Page View
The system SHALL provide a home page view at the root URL (`/`) that returns a welcome response. The template SHALL use semantic HTML elements, external CSS classes for styling, and accessibility attributes.

#### Scenario: Accessing the home page
- **WHEN** user sends a GET request to `/`
- **THEN** the system returns an HTTP 200 response containing a welcome message rendered with semantic HTML and external CSS styling

### Requirement: Event List View
The system SHALL provide an event list view that returns all events in the database. The template SHALL display events using semantic HTML (`<article>` or structured list items) with CSS classes for layout.

#### Scenario: Viewing the event list with events present
- **WHEN** user sends a GET request to `/events/`
- **THEN** the system returns an HTTP 200 response containing a list of all events rendered with semantic HTML elements and CSS classes

#### Scenario: Viewing the event list with no events
- **WHEN** user sends a GET request to `/events/` and no events exist
- **THEN** the system returns an HTTP 200 response indicating that no events are available

### Requirement: Event Detail View
The system SHALL provide an event detail view that returns the full details of a single event by its ID. The template SHALL use a definition list or structured semantic markup for event attributes.

#### Scenario: Viewing an existing event
- **WHEN** user sends a GET request to `/events/<event_id>/` with a valid event ID
- **THEN** the system returns an HTTP 200 response containing the event's title, description, date, location, category, and creator rendered with semantic HTML

#### Scenario: Viewing a non-existent event
- **WHEN** user sends a GET request to `/events/<event_id>/` with an ID that does not exist
- **THEN** the system returns an HTTP 404 response

### Requirement: Event Create Form View
The system SHALL provide a view at `/events/create/` that responds to GET requests by rendering an HTML form for event creation. Form controls SHALL use `<label>` elements with proper `for`/`id` associations, CSS classes for layout, and no inline styles.

#### Scenario: Accessing the event creation page while authenticated
- **WHEN** an authenticated user sends a GET request to `/events/create/`
- **THEN** the system returns an HTTP 200 response containing the HTML event creation form with accessible labels, CSS class styling, and a CSRF token

#### Scenario: Accessing the event creation page while unauthenticated
- **WHEN** an unauthenticated user sends a GET request to `/events/create/`
- **THEN** the system redirects the user to the login page

### Requirement: User Registration Form View
The system SHALL provide a view at `/users/register/` that responds to GET requests by rendering an HTML form for user creation. The form SHALL use `<label>` elements with proper `for`/`id` associations and CSS classes for styling.

#### Scenario: Accessing the user registration page
- **WHEN** user sends a GET request to `/users/register/`
- **THEN** the system returns an HTTP 200 response containing the HTML user registration form with accessible labels and CSS class styling

### Requirement: User Login Handler
The system SHALL provide a view at `/users/login/` that renders a login form on GET requests and authenticates the user on POST requests. The form SHALL use `<label>` elements with proper `for`/`id` associations and CSS classes for styling.

#### Scenario: Accessing the login page
- **WHEN** user sends a GET request to `/users/login/`
- **THEN** the system returns an HTTP 200 response containing the login form with accessible labels and CSS class styling

#### Scenario: User logs in successfully
- **WHEN** user sends a POST request with valid credentials to `/users/login/`
- **THEN** the system authenticates the user, creates a session, and redirects to the home page
