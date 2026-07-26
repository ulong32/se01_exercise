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
The system SHALL provide a dynamic search interaction on the event list page where typing in the search input triggers a partial page update of the event results without a full-page reload. The search input MUST use `hx-get` to send a GET request to the event list URL, `hx-trigger` with input debounce to avoid excessive requests, and `hx-target` to replace only the event results container.

#### Scenario: User types a search query
- **WHEN** a user types a search query into the search input on the event list page
- **THEN** after a debounce delay, the system sends a GET request with the query parameter and replaces only the event results area with the server response, without reloading the full page

#### Scenario: User clears the search input
- **WHEN** a user clears the search input
- **THEN** the system sends a GET request without a query parameter and the event results area updates to show all events

#### Scenario: JavaScript is disabled
- **WHEN** a user accesses the event list page with JavaScript disabled
- **THEN** the search form submits as a normal GET request and the full page reloads with filtered results (progressive enhancement)

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
