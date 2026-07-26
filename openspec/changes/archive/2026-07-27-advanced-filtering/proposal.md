## Why

The event listing page (`/events/`) currently supports only title substring search (`title__icontains`). Users cannot filter events by date range, category, or location — all of which are fields already present on the `Event` model. For a local event discovery application, multi-criteria filtering is a core usability requirement that directly impacts whether users can find relevant events.

## What Changes

- **New selector layer**: Create `apps/events/selectors.py` with a `get_events()` function encapsulating all read/query logic (per AGENTS.md convention: query logic belongs in selectors, not views).
- **Extended view parameters**: Update `event_list` view to accept and forward `category`, `date_from`, `date_to`, and `location` GET parameters to the selector.
- **Filter UI controls**: Add category dropdown, date range pickers, and location text input to the event list template, wired with HTMX attributes for seamless partial updates.
- **HTMX multi-input coordination**: Use `hx-include` to ensure all filter inputs (including the existing title search) are sent together on any filter change, preventing stale/partial filter state.
- **Test coverage**: Add tests for individual and combined filtering, ensuring pagination compatibility.

## Capabilities

### New Capabilities

_(none — filtering is an extension of existing event listing, not a standalone capability)_

### Modified Capabilities

- `htmx-dynamic-search`: Requirements expand from title-only search to multi-criteria filtering (category, date range, location). The HTMX interaction contract changes: multiple inputs now trigger partial updates, and all filter values must be included in each request.
- `basic-views`: The event list view requirement changes to accept additional query parameters and delegate to a selector function rather than inline ORM queries.

## Impact

- **`apps/events/selectors.py`** — new file (selector layer)
- **`apps/events/views.py`** — `event_list` refactored to use selector; parses new GET params
- **`apps/events/templates/events/event_list.html`** — new filter controls with HTMX attributes
- **`apps/events/templates/events/_event_results.html`** — no structural changes expected (results rendering stays the same)
- **`apps/events/tests.py`** — new test cases for filtering
- **`openspec/specs/htmx-dynamic-search/spec.md`** — updated requirements
- **`openspec/specs/basic-views/spec.md`** — updated event list view requirement
- **No model changes** — all needed fields (`date`, `location`, `category`) already exist
- **No URL pattern changes** — filtering uses GET parameters on the existing `/events/` endpoint
- **No API field renames** — existing `q` parameter preserved alongside new parameters
