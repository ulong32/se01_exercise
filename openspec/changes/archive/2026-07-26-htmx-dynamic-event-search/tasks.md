## 1. HTMX Library Setup

- [x] 1.1 Add HTMX CDN `<script>` tag to `templates/base.html` (before closing `</body>` tag)

## 2. Partial Template Extraction

- [x] 2.1 Create `apps/events/templates/events/_event_results.html` containing the event list `<ul>` markup (extracted from `event_list.html`)
- [x] 2.2 Update `apps/events/templates/events/event_list.html` to `{% include "events/_event_results.html" %}` instead of inline markup

## 3. HTMX Attributes on Search Input

- [x] 3.1 Add `hx-get`, `hx-trigger="input changed delay:300ms, search"`, `hx-target="#event-results"`, and `hx-swap="outerHTML"` attributes to the search input in `event_list.html`
- [x] 3.2 Add `id="event-results"` to the `<ul class="event-list">` wrapper in `_event_results.html`
- [x] 3.3 Add `name="q"` attribute is already present on the search input (verify)

## 4. Server-Side HTMX Detection

- [x] 4.1 Update `apps/events/views.py::event_list` to check for `HX-Request` header and render only `_event_results.html` for HTMX requests

## 5. CSS Loading Indicator (Optional Polish)

- [x] 5.1 Add CSS rule for `.htmx-request` class to show a subtle loading state on the results container (e.g., reduced opacity)

## 6. Verification

- [x] 6.1 Manual test: type in search input and verify results update without full-page reload
- [x] 6.2 Manual test: disable JavaScript and verify the form still works via normal GET submission
- [x] 6.3 Manual test: clear the search input and verify all events are shown again
- [x] 6.4 Add or update automated test for `event_list` view to verify partial HTML response when `HX-Request` header is present
