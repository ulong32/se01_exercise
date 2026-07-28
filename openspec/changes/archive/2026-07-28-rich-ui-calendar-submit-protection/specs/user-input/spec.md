## MODIFIED Requirements

### Requirement: User Input Forms
The system SHALL provide HTML forms for users to input data. Forms that retrieve or filter data MUST use the GET method, while forms that mutate state (create, update, delete) MUST use the POST method. All state-mutating forms MUST include the `data-submit-protect` attribute to enable frontend submit protection.

#### Scenario: Submitting a search query
- **WHEN** user submits a search or filter form
- **THEN** the browser sends a GET request with form data in the query string

#### Scenario: Submitting a creation form
- **WHEN** user submits a form to create a new entity
- **THEN** the browser sends a POST request with form data in the request body

#### Scenario: State-mutating form has submit protection
- **WHEN** reviewing any state-mutating form template (event create, event edit)
- **THEN** the `<form>` element includes the `data-submit-protect` attribute

## ADDED Requirements

### Requirement: Calendar Widget for Date/Time Fields
The system SHALL use Flatpickr as a visual calendar/datetime picker on all date/time input fields in event creation and editing forms. Flatpickr SHALL be configured with `enableTime: true` and `dateFormat: "Y-m-d\TH:i"` to produce ISO 8601 datetime strings compatible with Django's `parse_datetime`. The underlying `<input>` element SHALL retain `type="datetime-local"` as a fallback if Flatpickr fails to load.

#### Scenario: Date/time input uses Flatpickr
- **WHEN** the event create or edit form is rendered in a browser with JavaScript enabled
- **THEN** the date/time input field displays a Flatpickr calendar/time picker widget

#### Scenario: Flatpickr fallback
- **WHEN** Flatpickr CDN fails to load
- **THEN** the date/time input falls back to the browser's native `datetime-local` input
