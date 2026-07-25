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
The system SHALL provide a view at `/events/create/` that responds to GET requests by rendering an HTML form for event creation, including inputs for all required fields and a CSRF token.

#### Scenario: Accessing the event creation page while authenticated
- **WHEN** an authenticated user sends a GET request to `/events/create/`
- **THEN** the system returns an HTTP 200 response containing the HTML event creation form with a CSRF token

#### Scenario: Accessing the event creation page while unauthenticated
- **WHEN** an unauthenticated user sends a GET request to `/events/create/`
- **THEN** the system redirects the user to the login page

### Requirement: Event Create Handler
The system SHALL provide a handler at `/events/create/` that processes POST requests from the HTML form to create a new event. It MUST validate that all required fields are provided before creating the event in the database.

#### Scenario: Creating an event with valid data while authenticated
- **WHEN** an authenticated user sends a POST request to `/events/create/` with valid title, description, date, location, and category_id
- **THEN** the system creates a new Event in the database and redirects to the event detail page

#### Scenario: Creating an event while unauthenticated
- **WHEN** an unauthenticated user sends a POST request to `/events/create/`
- **THEN** the system redirects the user to the login page or returns a 403 Forbidden response

#### Scenario: Creating an event with missing required fields
- **WHEN** an authenticated user sends a POST request to `/events/create/` with missing required fields
- **THEN** the system returns an HTTP 400 response indicating the missing fields

### Requirement: Events URL Routing
The system SHALL define URL patterns in `apps/events/urls.py` and include them in the project-level URL configuration.

#### Scenario: URL namespace resolution
- **WHEN** any event-related URL is accessed
- **THEN** it is routed through the `events` app URL configuration under the `events` namespace

### Requirement: User Registration Form View
The system SHALL provide a view at `/users/register/` (or similar endpoint) that responds to GET requests by rendering an HTML form for user creation.

#### Scenario: Accessing the user registration page
- **WHEN** user sends a GET request to `/users/register/`
- **THEN** the system returns an HTTP 200 response containing the HTML user registration form

### Requirement: User Registration Handler
The system SHALL provide a handler at `/users/register/` that processes POST requests from the registration form to create a new user.

#### Scenario: Registering a user with valid data
- **WHEN** user sends a POST request to `/users/register/` with valid username and password
- **THEN** the system creates a new User in the database and redirects to the home page or login page

### Requirement: User Login Handler
The system SHALL provide a view at `/users/login/` that renders a login form on GET requests and authenticates the user on POST requests.

#### Scenario: User logs in successfully
- **WHEN** user sends a POST request with valid credentials to `/users/login/`
- **THEN** the system authenticates the user, creates a session, and redirects to the home page

### Requirement: User Logout Handler
The system SHALL provide a view at `/users/logout/` that terminates the user's session when a POST request is received.

#### Scenario: User logs out
- **WHEN** an authenticated user sends a POST request to `/users/logout/`
- **THEN** the system terminates the session and redirects to the home page
