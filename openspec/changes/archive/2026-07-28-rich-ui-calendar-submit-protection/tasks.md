## 1. Backend: Event Model & Deduplication Logic

- [x] 1.1 Add `created_at` field (`models.DateTimeField(auto_now_add=True)`) to `Event` model in `apps/events/models.py`
- [x] 1.2 Generate and apply database migration for the new `created_at` field
- [x] 1.3 Implement time-window deduplication logic in `create_event` in `apps/events/services.py` (check for matching `title`, `creator`, and `date` within 5 seconds)

## 2. Frontend: Flatpickr Calendar Widgets & Submit Protection

- [x] 2.1 Add Flatpickr CSS and JS CDN links to `templates/base.html`
- [x] 2.2 Add Flatpickr customisation rules and `.is-submitting` button loading state rules to `static/css/styles.css`
- [x] 2.3 Update `apps/events/templates/events/event_create.html` to include `data-submit-protect` attribute and initialize Flatpickr on `#date`
- [x] 2.4 Update `apps/events/templates/events/event_edit.html` to include `data-submit-protect` attribute and initialize Flatpickr on `#date`
- [x] 2.5 Add shared vanilla JS for submit button protection (disabling button and changing text/class on form submit) in `templates/base.html` or template blocks

## 3. Testing & Verification

- [x] 3.1 Write unit test in `apps/events/tests.py` verifying that duplicate event creation requests within the 5-second window return the existing event without creating a duplicate
- [x] 3.2 Write unit test verifying legitimate events with the same title/date created outside the window (or by a different user) are created successfully
- [x] 3.3 Run `pytest` to ensure all tests (existing and new) pass cleanly
