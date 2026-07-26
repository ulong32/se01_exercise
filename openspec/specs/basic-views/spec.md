# basic-views Specification

## Requirements

### Requirement: Home Page View
The system SHALL provide a home page view at the root URL (`/`) that returns a welcome response. The template SHALL use semantic HTML elements, external CSS classes for styling, and accessibility attributes.

#### Scenario: Accessing the home page
- **WHEN** user sends a GET request to `/`
- **THEN** the system returns an HTTP 200 response containing a welcome message rendered with semantic HTML and external CSS styling

### Requirement: Event List View
The system SHALL provide an event list view that accepts GET parameters `q` (title keyword), `category` (category ID), `date_from` (date string), `date_to` (date string), and `location` (location keyword) to filter events. The view SHALL delegate all query logic to a selector function in `apps/events/selectors.py` rather than performing inline ORM queries. The view SHALL parse and validate filter parameters, converting date strings to date objects and category strings to integer IDs, silently ignoring invalid values. The view SHALL pass the list of all categories and the current filter parameter values in the template context for full-page renders. The view SHALL detect HTMX requests via the `HX-Request` header and return only the event results partial template for HTMX requests, while returning the full page template for normal requests.

#### Scenario: Viewing the event list with events present
- **WHEN** user sends a GET request to `/events/`
- **THEN** the system returns an HTTP 200 response containing a list of all events and filter controls with all available categories rendered in the category dropdown

#### Scenario: Viewing the event list with no events
- **WHEN** user sends a GET request to `/events/` and no events exist
- **THEN** the system returns an HTTP 200 response indicating that no events are available, with filter controls still rendered

#### Scenario: Filtering by category
- **WHEN** user sends a GET request to `/events/?category=3`
- **THEN** the system returns only events belonging to the category with ID 3

#### Scenario: Filtering by date range
- **WHEN** user sends a GET request to `/events/?date_from=2026-07-01&date_to=2026-07-31`
- **THEN** the system returns only events whose date falls within July 1–31, 2026 (inclusive, date-only comparison ignoring time)

#### Scenario: Filtering by location keyword
- **WHEN** user sends a GET request to `/events/?location=tokyo`
- **THEN** the system returns only events whose location field contains "tokyo" (case-insensitive substring match)

#### Scenario: Combined filtering
- **WHEN** user sends a GET request to `/events/?q=workshop&category=2&date_from=2026-07-01&location=shibuya`
- **THEN** the system returns only events matching ALL specified criteria (AND logic)

#### Scenario: Invalid filter values are ignored
- **WHEN** user sends a GET request to `/events/?category=abc&date_from=not-a-date`
- **THEN** the system ignores the invalid parameters and returns unfiltered results for those criteria

#### Scenario: HTMX search request returns partial HTML
- **WHEN** user sends a GET request to `/events/` with the `HX-Request: true` header and any combination of filter parameters
- **THEN** the system returns an HTTP 200 response containing only the event results HTML fragment matching the filter criteria

### Requirement: Event Query Selector
The system SHALL provide a selector function `get_events()` in `apps/events/selectors.py` that accepts keyword-only arguments `query`, `category_id`, `date_from`, `date_to`, and `location`, all optional (defaulting to `None`). The function SHALL return a Django QuerySet of Event objects filtered by the provided criteria using AND logic. When `query` is provided, events SHALL be filtered by `title__icontains`. When `category_id` is provided, events SHALL be filtered by `category_id` exact match. When `date_from` is provided, events SHALL be filtered by `date__date__gte`. When `date_to` is provided, events SHALL be filtered by `date__date__lte`. When `location` is provided, events SHALL be filtered by `location__icontains`. The function SHALL return `Event.objects.all()` when no filter criteria are provided.

#### Scenario: No filters applied
- **WHEN** `get_events()` is called with no arguments
- **THEN** it returns a QuerySet containing all events

#### Scenario: Title keyword filter
- **WHEN** `get_events(query="workshop")` is called
- **THEN** it returns a QuerySet of events whose title contains "workshop" (case-insensitive)

#### Scenario: Category filter
- **WHEN** `get_events(category_id=3)` is called
- **THEN** it returns a QuerySet of events belonging to category with ID 3

#### Scenario: Date range filter
- **WHEN** `get_events(date_from=date(2026, 7, 1), date_to=date(2026, 7, 31))` is called
- **THEN** it returns a QuerySet of events whose date falls within July 1–31, 2026 (inclusive)

#### Scenario: Location filter
- **WHEN** `get_events(location="tokyo")` is called
- **THEN** it returns a QuerySet of events whose location contains "tokyo" (case-insensitive)

#### Scenario: Multiple filters combined
- **WHEN** `get_events(query="party", category_id=1, location="shibuya")` is called
- **THEN** it returns a QuerySet of events matching all three criteria (AND logic)

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
The system SHALL provide a view at `/users/register/` (or similar endpoint) that responds to GET requests by rendering an HTML form for user creation. The form SHALL use `<label>` elements with proper `for`/`id` associations and CSS classes for styling.

#### Scenario: Accessing the user registration page
- **WHEN** user sends a GET request to `/users/register/`
- **THEN** the system returns an HTTP 200 response containing the HTML user registration form with accessible labels and CSS class styling

### Requirement: User Registration Handler
The system SHALL provide a handler at `/users/register/` that processes POST requests from the registration form to create a new user.

#### Scenario: Registering a user with valid data
- **WHEN** user sends a POST request to `/users/register/` with valid username and password
- **THEN** the system creates a new User in the database and redirects to the home page or login page

### Requirement: User Login Handler
The system SHALL provide a view at `/users/login/` that renders a login form on GET requests and authenticates the user on POST requests. The form SHALL use `<label>` elements with proper `for`/`id` associations and CSS classes for styling.

#### Scenario: Accessing the login page
- **WHEN** user sends a GET request to `/users/login/`
- **THEN** the system returns an HTTP 200 response containing the login form with accessible labels and CSS class styling

#### Scenario: User logs in successfully
- **WHEN** user sends a POST request with valid credentials to `/users/login/`
- **THEN** the system authenticates the user, creates a session, and redirects to the home page

### Requirement: User Logout Handler
The system SHALL provide a view at `/users/logout/` that terminates the user's session when a POST request is received.

#### Scenario: User logs out
- **WHEN** an authenticated user sends a POST request to `/users/logout/`
- **THEN** the system terminates the session and redirects to the home page
