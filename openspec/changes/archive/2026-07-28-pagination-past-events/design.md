## Context

The event listing page (`/events/`) currently fetches the entire `Event` queryset without pagination. The view delegates filtering to `get_events()` in `apps/events/selectors.py` and uses HTMX for partial page updates via `_event_results.html`. There is no concept of "past events"—all events are displayed identically regardless of whether their date has passed.

Key constraints from the existing architecture:
- HTMX partial updates swap `#event-results` via `outerHTML`; pagination controls must live **inside** this container.
- All filter inputs use `hx-include="closest form"` to send the full form state; pagination links must also carry the current page and filter values.
- The project convention places query logic in `selectors.py` and keeps views thin.

## Goals / Non-Goals

**Goals:**
- Paginate the event list with Django's `Paginator` (12 events per page).
- Ensure pagination navigation works seamlessly with HTMX partial updates **and** full-page loads (progressive enhancement).
- Preserve all active filter/search query parameters across page transitions.
- Exclude past events by default; provide an "Include past events" toggle that integrates with the existing HTMX filter flow.
- Visually distinguish past events (when shown) with reduced-opacity gray-out styling.
- Add comprehensive test coverage for pagination, past-event filtering, and their combination with existing filters.

**Non-Goals:**
- Infinite scroll or load-more patterns (standard page-number navigation only).
- Changing the Event model schema (no new fields or migrations needed).
- Server-side caching of paginated results.
- Cursor-based pagination (offset-based via `Paginator` is sufficient at current scale).

## Decisions

### 1. Pagination lives inside `_event_results.html`

**Decision**: Pagination navigation controls will be rendered inside the `_event_results.html` partial, below the event grid.

**Rationale**: Since HTMX swaps `#event-results` via `outerHTML`, any pagination controls outside this container would become stale after a partial update. Placing them inside ensures they are always re-rendered with the correct page context.

**Alternative considered**: Separate pagination partial included in both the full page and the HTMX response—rejected because it adds template complexity for no benefit.

### 2. Pagination links use HTMX attributes with `hx-include`

**Decision**: Each pagination link (`<a>`) will carry `hx-get` with the `page` parameter, `hx-target="#event-results"`, `hx-swap="outerHTML"`, and `hx-include="[form.search-form]"` (the search form) to carry all active filters.

**Rationale**: Using `hx-include` on the pagination links themselves (pointing to the form) ensures that whatever the user has typed/selected in the filter controls is included in the pagination request, without duplicating query parameters in the URL. This also means the `page` parameter is the **only** parameter in the `hx-get` URL itself, keeping it clean.

**Alternative considered**: Encoding all filters into query parameters on each pagination link—rejected because the filter values can change on the client side (the user may have typed something new) and stale query params would override live form values.

### 3. Past events filtering via `include_past` GET parameter and selector kwarg

**Decision**: Add an `include_past: bool` parameter to `get_events()`. When `False` (default), events with `date < now()` are excluded. The view reads `include_past` from the GET query string. The UI provides a checkbox `<input type="checkbox" name="include_past" value="true">` inside the existing search form with HTMX `hx-trigger="change"`.

**Rationale**: This follows the existing pattern of filter parameters being GET params processed by the view and delegated to the selector. A checkbox integrates naturally with `hx-include="closest form"`.

**Alternative considered**: Annotating each event with `is_past` and filtering in the template—rejected because it wastes a database query on events that will be hidden, and doesn't interact well with pagination counts.

### 4. Visual gray-out with `.past-event` CSS class

**Decision**: When `include_past=true`, past event `<article>` elements receive an additional `past-event` class. CSS applies `opacity: 0.6; filter: grayscale(60%);` and reduces hover effects.

**Rationale**: Pure CSS approach—no JavaScript needed. The template can conditionally add the class by comparing `event.date` to `now` using Django's `{% now %}` or by passing `now` in the template context.

**Implementation detail**: Pass `now` timestamp in the template context from the view. The template uses `{% if event.date < now %}` to conditionally add the class. This is more reliable than using `{% now %}` tag which produces a string.

### 5. Page size of 12

**Decision**: Default to 12 events per page.

**Rationale**: 12 is divisible by the CSS grid column counts (1, 2, 3, 4), keeping the grid visually balanced at all breakpoints. The Issue suggested 10–20; 12 is the sweet spot.

## Risks / Trade-offs

- **Pagination + filter parameter preservation is fragile** (noted in `AGENTS.md`): Using `hx-include` to read live form values mitigates stale-parameter bugs, but tests must cover combined filter+pagination scenarios thoroughly. → Mitigation: Dedicated test cases for multi-filter + page-2+ scenarios.

- **Past event exclusion changes default behavior**: Users who previously saw all events will now only see upcoming ones by default. → Mitigation: The "Include past events" checkbox is prominent and its state is preserved across HTMX updates via the form.

- **Template `{% if event.date < now %}` comparison**: Requires timezone-aware `now` value in context. If accidentally passed as naive datetime, comparison will fail or warn. → Mitigation: Use `django.utils.timezone.now()` consistently.
