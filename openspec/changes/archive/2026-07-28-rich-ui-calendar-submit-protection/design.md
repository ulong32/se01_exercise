## Context

The Event Listings application uses Django server-rendered templates with HTMX for dynamic updates. Event create/edit forms currently use browser-native `<input type="datetime-local">`, which works but has inconsistent UX across browsers. The base template already loads HTMX from CDN. There is no frontend or backend protection against duplicate form submissions beyond the PRG pattern.

Currently, `services.py` contains simple `create_event` / `update_event` functions with no deduplication logic. The `Event` model has no fields for tracking submission idempotency.

## Goals / Non-Goals

**Goals:**
- Provide a rich, consistent calendar/datetime picker experience across all browsers using Flatpickr.
- Prevent duplicate event creation/editing from rapid double-clicks via frontend button disabling and a backend time-window deduplication guard.
- Maintain full compatibility with existing HTMX-driven search and filter workflows.
- Keep all styling in `static/css/styles.css` (no inline styles).
- Add comprehensive backend tests for deduplication behavior.

**Non-Goals:**
- A full calendar view page (`/events/calendar/`) — listed as optional in the issue, deferred to a separate change.
- Token-based idempotency keys (too complex for this scope; time-window check is sufficient).
- Replacing the Django view-based form handling with Django Forms / ModelForms.

## Decisions

### Decision 1: Flatpickr via CDN for calendar widgets

**Choice**: Load Flatpickr CSS and JS from CDN (cdnjs) in `base.html`, initialise on `datetime-local` inputs in create/edit templates via inline `<script>` blocks.

**Alternatives considered**:
- **HTML5 `<input type="datetime-local">` only**: Already in use; cross-browser UX is inconsistent (e.g., Firefox vs Chrome differences). Rejected.
- **Bundled via npm/webpack**: The project has no JS build pipeline; adding one is excessive for this use case.
- **Other libraries (Pikaday, Litepicker)**: Flatpickr is more mature, supports datetime (not just date), is lightweight (~16KB min+gz), and has zero dependencies.

**Rationale**: CDN loading aligns with how HTMX is already loaded. Flatpickr is configured with `enableTime: true` and `dateFormat: "Y-m-d\\TH:i"` to produce ISO 8601 strings that `parse_datetime` already expects.

### Decision 2: Frontend submit protection via vanilla JS

**Choice**: Add a `<script>` block (or a shared JS file) that attaches `submit` event listeners to forms with a `data-submit-protect` attribute. On submit, the button is disabled, text changes to "Submitting…", and a CSS class `.is-submitting` is applied to show a loading spinner.

**Alternatives considered**:
- **HTMX `hx-disable-elt`**: Only works for HTMX-driven requests; create/edit forms use standard POST.
- **Per-template inline JS**: Works but duplicates code. A shared approach via `data-submit-protect` attribute is DRYer.

**Rationale**: Vanilla JS keeps the solution simple and framework-agnostic. The `data-submit-protect` attribute pattern makes it opt-in per form.

### Decision 3: Backend deduplication via time-window check

**Choice**: In `create_event()` in `services.py`, before creating, check if an event with the same `title + creator + date` was created within the last 5 seconds. If so, return the existing event instead of creating a duplicate.

**Alternatives considered**:
- **Unique constraint on (title, creator, date)**: Too restrictive — legitimate events with the same title/date by the same creator are possible over time.
- **Idempotency token (CSRF-based or custom UUID)**: More robust but adds complexity (session storage, token management). Overkill for this use case.
- **Database-level advisory lock**: Too low-level for Django's ORM patterns.

**Rationale**: Time-window deduplication is simple, effective for rapid double-click scenarios, and requires no schema changes. The `Event` model's `auto_now_add` field (if added) or a filter on `date` creation timestamp handles the window check. Since `Event` has no `created_at` field, we'll add one.

### Decision 4: Add `created_at` field to Event model

**Choice**: Add `created_at = models.DateTimeField(auto_now_add=True)` to the `Event` model for deduplication timestamp queries.

**Rationale**: This field is generally useful (e.g., sorting by creation time) and enables the time-window deduplication query in `create_event`. A new migration will be created.

## Risks / Trade-offs

- **[CDN availability]** → Flatpickr loaded from CDN; if CDN is down, the native `datetime-local` input remains functional as fallback since we keep `type="datetime-local"` on the input element.
- **[5-second dedup window]** → May occasionally block a legitimate rapid re-creation. Mitigated by returning the existing event (no error) and the fact that truly identical events within 5 seconds are extremely unlikely to be intentional.
- **[No `created_at` on existing events]** → Migration will set `default=timezone.now` for existing rows. Acceptable since deduplication only matters for future submissions.
- **[JS loading order]** → Flatpickr init scripts must run after DOM is ready. We'll use `DOMContentLoaded` listeners or place scripts at the end of the template body.
