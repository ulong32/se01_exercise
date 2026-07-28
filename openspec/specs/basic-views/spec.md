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

### Requirement: Event List Pagination
The system SHALL paginate the event list using Django's `Paginator` with a default page size of 12 events per page. The view SHALL accept a `page` GET parameter to select the page number. The view SHALL pass the Django `Page` object to the template context as `page_obj`. When an invalid or out-of-range page number is provided, the view SHALL fall back to page 1.

#### Scenario: Default pagination (page 1)
- **WHEN** user sends a GET request to `/events/` without a `page` parameter
- **THEN** the system returns the first 12 events (ordered by the default queryset ordering) and pagination controls indicating the current page is 1

#### Scenario: Accessing a specific page
- **WHEN** user sends a GET request to `/events/?page=3`
- **THEN** the system returns the third page of 12 events and pagination controls indicating the current page is 3

#### Scenario: Invalid page number falls back to page 1
- **WHEN** user sends a GET request to `/events/?page=abc` or `/events/?page=999` (exceeding total pages)
- **THEN** the system returns page 1 of the paginated results without an error

#### Scenario: Pagination combined with filters
- **WHEN** user sends a GET request to `/events/?q=workshop&category=2&page=2`
- **THEN** the system returns the second page of events matching the filter criteria, with pagination controls reflecting the filtered result count

#### Scenario: HTMX pagination request returns partial HTML
- **WHEN** user sends a GET request to `/events/?page=2` with the `HX-Request: true` header
- **THEN** the system returns only the event results HTML fragment including updated pagination controls, not the full page

### Requirement: Past Events Filtering
The system SHALL exclude past events (events whose `date` is earlier than the current time) from the event list by default. The view SHALL accept an `include_past` GET parameter; when its value is `"true"`, past events SHALL be included in the results. The `get_events()` selector function SHALL accept an `include_past` keyword-only argument (default `False`). When `include_past` is `False`, the selector SHALL filter the queryset to include only events with `date >= now()`.

#### Scenario: Default listing excludes past events
- **WHEN** user sends a GET request to `/events/` without an `include_past` parameter
- **THEN** the system returns only events whose date is in the future (relative to the current server time)

#### Scenario: Including past events via parameter
- **WHEN** user sends a GET request to `/events/?include_past=true`
- **THEN** the system returns all events including those whose date has passed

#### Scenario: Past events toggle with other filters
- **WHEN** user sends a GET request to `/events/?category=2&include_past=true`
- **THEN** the system returns all events (including past) matching the category filter

### Requirement: Past Event Visual Distinction
The system SHALL visually distinguish past events from upcoming events when past events are displayed. Each past event card SHALL receive a CSS class `past-event` that applies reduced opacity and grayscale styling. The view SHALL pass a timezone-aware `now` value in the template context for date comparison.

#### Scenario: Past event card is visually grayed out
- **WHEN** the event list is rendered with `include_past=true` and the list contains events whose date has passed
- **THEN** each past event's `<article>` element has the CSS class `past-event` applied, rendering it with reduced opacity and grayscale effect

#### Scenario: Upcoming event card has normal styling
- **WHEN** the event list is rendered and an event's date is in the future
- **THEN** the event's `<article>` element does NOT have the `past-event` class

### Requirement: Event Query Selector
The system SHALL provide a selector function `get_events()` in `apps/events/selectors.py` that accepts keyword-only arguments `query`, `category_id`, `date_from`, `date_to`, `location`, and `include_past`, all optional (defaulting to `None` except `include_past` which defaults to `False`). The function SHALL return a Django QuerySet of Event objects filtered by the provided criteria using AND logic. When `query` is provided, events SHALL be filtered by `title__icontains`. When `category_id` is provided, events SHALL be filtered by `category_id` exact match. When `date_from` is provided, events SHALL be filtered by `date__date__gte`. When `date_to` is provided, events SHALL be filtered by `date__date__lte`. When `location` is provided, events SHALL be filtered by `location__icontains`. When `include_past` is `False`, events SHALL be filtered by `date__gte=now()` using `django.utils.timezone.now()`. The function SHALL return `Event.objects.all()` (with the past-event filter still applied when `include_past` is `False`) when no other filter criteria are provided.

#### Scenario: No filters applied
- **WHEN** `get_events()` is called with no arguments
- **THEN** it returns a QuerySet containing only upcoming events (date >= now)

#### Scenario: Title keyword filter
- **WHEN** `get_events(query="workshop")` is called
- **THEN** it returns a QuerySet of upcoming events whose title contains "workshop" (case-insensitive)

#### Scenario: Category filter
- **WHEN** `get_events(category_id=3)` is called
- **THEN** it returns a QuerySet of upcoming events belonging to category with ID 3

#### Scenario: Date range filter
- **WHEN** `get_events(date_from=date(2026, 7, 1), date_to=date(2026, 7, 31))` is called
- **THEN** it returns a QuerySet of events whose date falls within July 1–31, 2026 (inclusive), excluding past events unless include_past=True

#### Scenario: Location filter
- **WHEN** `get_events(location="tokyo")` is called
- **THEN** it returns a QuerySet of upcoming events whose location contains "tokyo" (case-insensitive)

#### Scenario: Multiple filters combined
- **WHEN** `get_events(query="party", category_id=1, location="shibuya")` is called
- **THEN** it returns a QuerySet of upcoming events matching all three criteria (AND logic)

#### Scenario: Include past events
- **WHEN** `get_events(include_past=True)` is called
- **THEN** it returns a QuerySet containing all events regardless of date

#### Scenario: Include past events with filters
- **WHEN** `get_events(query="meetup", include_past=True)` is called
- **THEN** it returns a QuerySet of all events (including past) whose title contains "meetup"

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
