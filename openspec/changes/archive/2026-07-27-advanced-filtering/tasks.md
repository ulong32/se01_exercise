## 1. Selector Layer

- [x] 1.1 Create `apps/events/selectors.py` with `get_events(*, query=None, category_id=None, date_from=None, date_to=None, location=None)` function that builds a filtered QuerySet using AND logic. Each parameter is independently optional; `None` means no filter for that criterion.
- [x] 1.2 Implement title filter: `title__icontains` when `query` is provided.
- [x] 1.3 Implement category filter: `category_id=category_id` exact match when `category_id` is provided.
- [x] 1.4 Implement date range filter: `date__date__gte=date_from` and `date__date__lte=date_to` when respective parameters are provided (date-only comparison).
- [x] 1.5 Implement location filter: `location__icontains` when `location` is provided.

## 2. View Updates

- [x] 2.1 Update `event_list` in `apps/events/views.py` to import and call `get_events()` from selectors instead of inline ORM queries.
- [x] 2.2 Parse GET parameters: `q` (str), `category` (int, silently ignore if invalid), `date_from` (date, silently ignore if unparseable), `date_to` (date, silently ignore if unparseable), `location` (str).
- [x] 2.3 Pass `categories` (all Category objects) and current filter values (`q`, `category`, `date_from`, `date_to`, `location`) in the template context for full-page renders.
- [x] 2.4 Preserve existing HTMX partial response behavior: return `_event_results.html` when `HX-Request` header is present.

## 3. Template Updates

- [x] 3.1 Update `apps/events/templates/events/event_list.html` to add filter controls inside the existing `<form>`: category `<select>` dropdown (name=`category`), `<input type="date">` for `date_from` and `date_to`, and text `<input>` for `location`.
- [x] 3.2 Add `<label>` elements with proper `for`/`id` associations for each new filter control (accessibility).
- [x] 3.3 Add HTMX attributes to new controls: `hx-get`, `hx-target="#event-results"`, `hx-swap="outerHTML"`, `hx-include="closest form"`. Use `hx-trigger="change"` for select/date inputs, `hx-trigger="input changed delay:300ms"` for text inputs.
- [x] 3.4 Pre-populate filter controls with current values from template context (for non-HTMX full-page loads) using `value="{{ ... }}"` and `selected` attribute on options.
- [x] 3.5 Add `hx-include="closest form"` to the existing search input so it sends all filter values when triggered.

## 4. Testing

- [x] 4.1 Add unit tests for `get_events()` selector: test each filter criterion individually (title, category, date range, location).
- [x] 4.2 Add unit tests for combined filter criteria (multiple filters active simultaneously, AND logic).
- [x] 4.3 Add integration tests for `event_list` view: test GET parameters are parsed and forwarded correctly, test invalid parameter handling (graceful degradation).
- [x] 4.4 Add integration test for HTMX partial response with filter parameters (verify `HX-Request` header triggers partial template with filtered results).
- [x] 4.5 Verify existing tests still pass (no regressions from the refactor).

## 5. Spec Documentation

- [x] 5.1 Sync delta specs to main specs after implementation is verified (via `/opsx-sync`).

## 6. Verification

- [x] 6.1 Run `pytest` and confirm all tests pass.
- [x] 6.2 Run `ruff check` and `ruff format` to ensure code quality.
- [x] 6.3 Manual smoke test: visit `/events/`, verify all filter controls render, test each filter individually and in combination, verify HTMX partial updates work, verify progressive enhancement (form submits work without JS).
