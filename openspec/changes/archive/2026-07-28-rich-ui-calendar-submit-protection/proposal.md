## Why

Event creation and editing forms currently use plain `<input type="datetime-local">` fields which, while functional, lack a polished calendar widget experience. More critically, there is no protection against duplicate form submissions — rapid clicks before the POST-Redirect-GET cycle completes can create duplicate event records. This impacts data integrity and user experience.

## What Changes

- **Calendar widgets on forms**: Integrate Flatpickr (lightweight, zero-dependency date/time picker) into `event_create.html` and `event_edit.html` to replace the browser-default `datetime-local` input with a visually rich, cross-browser-consistent calendar picker.
- **Submit protection (frontend)**: Add JavaScript logic to disable submit buttons on form submission and display a loading indicator, preventing double-clicks on event create/edit/delete forms.
- **Submit protection (backend)**: Add an idempotency mechanism in `services.py` using a time-window deduplication check — reject identical event creation requests from the same user within a short window (e.g., 5 seconds).
- **CSS additions**: Add styles for Flatpickr customisation overrides and submit-protection loading states in `static/css/styles.css` (no inline styles).
- **Tests**: Add backend tests verifying that duplicate submissions within the time window are rejected.

## Capabilities

### New Capabilities
- `submit-protection`: Frontend double-click prevention and backend idempotency guard for state-mutating forms.

### Modified Capabilities
- `user-input`: Add requirement for calendar widget on date/time form fields and submit protection behavior.
- `ui-styling`: Add requirement for calendar widget styling and submit-button loading-state styling.

## Impact

- **Templates**: `event_create.html`, `event_edit.html` — add Flatpickr initialization and submit protection JS.
- **Static assets**: `static/css/styles.css` — new CSS rules for calendar widget overrides and loading states.
- **Base template**: `templates/base.html` — add Flatpickr CSS/JS CDN links.
- **Services**: `apps/events/services.py` — add deduplication logic in `create_event`.
- **Tests**: `apps/events/tests.py` — new test cases for submit protection.
- **OpenSpec**: Delta specs for `user-input` and `ui-styling`; new spec for `submit-protection`.
