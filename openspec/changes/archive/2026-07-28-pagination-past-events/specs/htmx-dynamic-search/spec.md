## ADDED Requirements

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
