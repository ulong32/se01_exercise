## MODIFIED Requirements

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
