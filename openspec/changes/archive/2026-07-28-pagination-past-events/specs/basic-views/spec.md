## ADDED Requirements

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

## MODIFIED Requirements

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
