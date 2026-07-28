# htmx-dynamic-search Specification

## Purpose
Defines requirements for HTMX-driven dynamic partial updates and search interactivity.

## Requirements

### Requirement: HTMX Library Inclusion
The system SHALL include the HTMX JavaScript library in the base template so that HTMX attributes are available on all pages. The library MUST be loaded from a CDN via a `<script>` tag.

#### Scenario: HTMX is available on any page
- **WHEN** a user loads any page of the application
- **THEN** the HTMX library is loaded and HTMX attributes on HTML elements are functional

### Requirement: Dynamic Event Search via HTMX
The system SHALL provide a dynamic multi-criteria filtering interaction on the event list page. The page SHALL include filter controls for title keyword search, category selection, date range (from/to), and location keyword search. Changing any filter criterion SHALL trigger a partial page update of the event results via HTMX without a full-page reload. All filter inputs SHALL be enclosed in a single `<form>` element, and each input SHALL use `hx-get` to send a GET request to the event list URL with `hx-include="closest form"` to include all current filter values. Text inputs (title search, location) SHALL use `hx-trigger="input changed delay:300ms, search"` for debounced updates. Discrete inputs (category dropdown, date pickers) SHALL use `hx-trigger="change"` for immediate updates. All inputs SHALL use `hx-target="#event-results"` and `hx-swap="outerHTML"` to replace only the event results container.

#### Scenario: User types a search query
- **WHEN** a user types a search query into the title search input on the event list page
- **THEN** after a debounce delay, the system sends a GET request with the `q` parameter and all other current filter values, and replaces only the event results area with the server response

#### Scenario: User selects a category filter
- **WHEN** a user selects a category from the category dropdown
- **THEN** the system immediately sends a GET request with the selected `category` parameter and all other current filter values, and replaces only the event results area with matching events

#### Scenario: User sets a date range
- **WHEN** a user sets a `date_from` and/or `date_to` value using date picker inputs
- **THEN** the system immediately sends a GET request with the date range parameters and all other current filter values, and replaces only the event results area with events whose date falls within the specified range (inclusive, date-only comparison)

#### Scenario: User enters a location filter
- **WHEN** a user types a location keyword into the location filter input
- **THEN** after a debounce delay, the system sends a GET request with the `location` parameter and all other current filter values, and replaces only the event results area with events whose location contains the keyword (case-insensitive)

#### Scenario: User clears all filters
- **WHEN** a user clears all filter inputs (empty title, no category selected, no dates, empty location)
- **THEN** the system sends a GET request without filter parameters and the event results area updates to show all events

#### Scenario: Combined filters narrow results
- **WHEN** a user has multiple filters active simultaneously (e.g., category "Workshop" and location "Tokyo")
- **THEN** the system returns only events matching ALL active filter criteria (AND logic)

#### Scenario: JavaScript is disabled
- **WHEN** a user accesses the event list page with JavaScript disabled
- **THEN** the search form submits as a normal GET request with all filter parameters and the full page reloads with filtered results (progressive enhancement)

### Requirement: Filter Controls Layout
The system SHALL render filter controls on the event list page consisting of: a text input for title keyword search (name=`q`), a `<select>` dropdown for category selection (name=`category`) with a blank/all option, two `<input type="date">` fields for date range (name=`date_from`, name=`date_to`), and a text input for location keyword search (name=`location`). Each control SHALL have an associated `<label>` element with proper `for`/`id` association for accessibility.

#### Scenario: Filter controls are present on event list page
- **WHEN** a user loads the event list page
- **THEN** the page displays filter controls for title search, category dropdown (populated with all available categories), date range pickers, and location search input

#### Scenario: Category dropdown includes all categories
- **WHEN** the category dropdown is rendered
- **THEN** it contains an "All categories" option (value="") followed by one option per Category record in the database

#### Scenario: Filter values persist on full page load
- **WHEN** a user submits filters via standard GET (non-HTMX) and the page reloads
- **THEN** the filter controls retain the submitted values via the template context

### Requirement: Partial HTML Response for HTMX Requests
The system SHALL detect HTMX requests by checking for the `HX-Request` HTTP header. When the header is present, the event list view MUST return only the event results HTML fragment (partial template). When the header is absent, the view MUST return the full page as before.

#### Scenario: HTMX request receives partial HTML
- **WHEN** the event list view receives a GET request with the `HX-Request: true` header
- **THEN** the system returns an HTTP 200 response containing only the event results HTML fragment (no `<html>`, `<head>`, `<body>`, header, or footer markup)

#### Scenario: Normal request receives full page
- **WHEN** the event list view receives a GET request without the `HX-Request` header
- **THEN** the system returns the full HTML page including layout, header, and footer

### Requirement: Event Results Partial Template
The system SHALL provide a partial template (`_event_results.html`) containing only the event results list markup. The main event list template MUST use `{% include %}` to render this partial, ensuring the full-page and HTMX responses share the same HTML fragment.

#### Scenario: Partial template renders event cards
- **WHEN** the partial template is rendered with a list of events
- **THEN** it produces an HTML `<ul>` element with class `event-list` containing one `<li>` per event with title, description excerpt, date, and location

#### Scenario: Partial template renders empty state
- **WHEN** the partial template is rendered with no events
- **THEN** it produces an HTML `<ul>` element containing a single `<li>` with an empty-state message

### Requirement: HTMX Pagination Navigation
The system SHALL render pagination navigation controls inside the event results partial template (`_event_results.html`) so that HTMX partial updates include refreshed pagination links. Each pagination link SHALL use `hx-get` with the target page number as a `page` query parameter, `hx-target="#event-results"`, `hx-swap="outerHTML"`, and `hx-include="[form.search-form]"` to carry all active filter values from the search form. Pagination navigation SHALL include Previous/Next links and individual page number links.

#### Scenario: Clicking next page via HTMX
- **WHEN** user clicks the "Next" pagination link on the event list page
- **THEN** the system sends an HTMX GET request with the next page number and all current filter values, replacing only the event results container with the next page of results and updated pagination controls

#### Scenario: Clicking a specific page number via HTMX
- **WHEN** user clicks page number "3" in the pagination navigation
- **THEN** the system sends an HTMX GET request with `page=3` and all current filter values, replacing only the event results container with page 3 results

#### Scenario: Pagination preserves filter state across pages
- **WHEN** user has active filters (e.g., category=2, q=workshop) and clicks a pagination link
- **THEN** the HTMX request includes both the page number from the link and all current filter values from the form, returning correctly filtered and paginated results

#### Scenario: Pagination works without JavaScript (progressive enhancement)
- **WHEN** user accesses `/events/?page=2&q=workshop` with JavaScript disabled
- **THEN** the full page loads with page 2 of the filtered results and all filter controls retain their values

### Requirement: Include Past Events Toggle
The system SHALL render a checkbox control labeled "Include past events" inside the search form on the event list page. The checkbox SHALL have `name="include_past"` and `value="true"`. It SHALL use `hx-get`, `hx-trigger="change"`, `hx-target="#event-results"`, `hx-swap="outerHTML"`, and `hx-include="closest form"` to trigger a partial update when toggled. When checked, the request SHALL include `include_past=true`. The checkbox state SHALL be preserved across HTMX updates and full-page reloads via the template context.

#### Scenario: Toggling the past events checkbox on
- **WHEN** user checks the "Include past events" checkbox
- **THEN** the system sends an HTMX GET request with `include_past=true` and all other filter values, and the event results area updates to include past events (visually distinguished)

#### Scenario: Toggling the past events checkbox off
- **WHEN** user unchecks the "Include past events" checkbox
- **THEN** the system sends an HTMX GET request without `include_past` and all other filter values, and the event results area updates to show only upcoming events

#### Scenario: Past events checkbox state persists on full-page reload
- **WHEN** user accesses `/events/?include_past=true` via full page load
- **THEN** the checkbox is rendered in the checked state and past events are displayed
