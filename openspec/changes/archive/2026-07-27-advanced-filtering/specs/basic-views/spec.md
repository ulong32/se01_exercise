## MODIFIED Requirements

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

## ADDED Requirements

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
