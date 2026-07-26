## Context

The Event Listings application currently has a search feature on the event list page (`/events/`) that uses a traditional HTML `<form method="GET">` submission. When the user types a query and clicks "Search", the entire page reloads—header, footer, navigation, and all—just to update the event results.

The project uses Django server-rendered templates with a `base.html` layout. There is no JavaScript framework in place. The event list view (`apps/events/views.py::event_list`) already supports a `q` query parameter for title-based filtering.

## Goals / Non-Goals

**Goals:**
- Enable dynamic, partial-page updates for event search using HTMX.
- The event results area updates without a full-page reload when the user types or submits a search query.
- Maintain full functionality for users with JavaScript disabled (progressive enhancement via graceful degradation to normal form submit).
- Keep the implementation minimal and server-driven (no client-side rendering).

**Non-Goals:**
- Adding advanced filtering (date, category, location) in this change — that may come later.
- Client-side rendering with React/Vue/etc.
- Adding a REST/JSON API — the server returns HTML fragments.
- Pagination — existing behavior is preserved as-is.

## Decisions

### Decision 1: Use HTMX via CDN

**Choice**: Include HTMX via a CDN `<script>` tag in `base.html`.

**Alternatives considered**:
- **npm/bundled**: Requires a build pipeline that doesn't exist yet. Over-engineered for a single interaction.
- **Django-htmx package**: Adds a Python dependency and middleware. Useful for large projects but overkill here since we only need to check the `HX-Request` header.

**Rationale**: A CDN script tag is zero-config, instantly available, and trivially reversible. No build step, no new Python dependency.

### Decision 2: Detect HTMX requests via `HX-Request` header

**Choice**: In the `event_list` view, check `request.headers.get('HX-Request')` to determine if the request comes from HTMX. If yes, render only the partial template; otherwise, render the full page.

**Alternatives considered**:
- **Separate URL endpoint** (e.g., `/events/search/`): Creates a separate view and URL pattern. More surface area to maintain, and duplicates query logic.
- **django-htmx middleware**: Adds `request.htmx` attribute. Clean, but adds a dependency for a single header check.

**Rationale**: Checking the header directly is a one-liner, requires no dependencies, and keeps the search logic in a single view function.

### Decision 3: Extract event results into a partial template

**Choice**: Create `_event_results.html` containing only the `<ul class="event-list">...</ul>` block. The full `event_list.html` will `{% include %}` this partial. HTMX requests render only the partial.

**Rationale**: This avoids duplicating HTML markup. The full page and the HTMX response share the same fragment, ensuring consistency.

### Decision 4: Use `hx-trigger="input changed delay:300ms"` on the search input

**Choice**: Trigger the HTMX request on input with a 300ms debounce, plus on form submit.

**Alternatives considered**:
- **Only on submit**: Less interactive; user still has to click a button.
- **On keyup without debounce**: Fires too many requests, creating server load.
- **Longer debounce (500ms+)**: Feels sluggish.

**Rationale**: 300ms debounce strikes a balance between responsiveness and request volume. The `changed` modifier prevents duplicate requests for the same value.

### Decision 5: Use `hx-target` to swap only the results container

**Choice**: Add an `id="event-results"` to the `<ul class="event-list">` wrapper and set `hx-target="#event-results"` with `hx-swap="outerHTML"` on the search input.

**Rationale**: Only the results area gets replaced. The search form, heading, and page chrome remain untouched.

## Risks / Trade-offs

- **[CDN dependency]** → If the CDN is unreachable, HTMX won't load. Mitigation: The form still works normally via GET submission (progressive enhancement). Users without JS get the same experience as before.
- **[No loading indicator]** → Users may not notice the partial update is in progress. Mitigation: HTMX adds `htmx-request` class during requests; we can style this to show a subtle loading state via CSS. This is low-risk for a search that returns quickly.
- **[Search on input may expose partial queries in server logs]** → Mitigation: This is standard behavior for type-ahead search. No sensitive data is involved (just event titles).
