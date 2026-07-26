## Context

The event listing page (`/events/`) currently performs inline `title__icontains` filtering directly in the `event_list` view. The `Event` model already has `date` (DateTimeField), `location` (CharField), and `category` (FK to Category), but none are queryable from the UI. The project convention (AGENTS.md) requires reusable read/query logic in `selectors.py`, which does not yet exist for the events app. HTMX dynamic search is already wired for the title input; the new filters must integrate into the same HTMX partial-update flow.

## Goals / Non-Goals

**Goals:**

- Enable users to filter events by any combination of: title keyword, category, date range (from/to), and location keyword.
- Introduce `apps/events/selectors.py` as the canonical query layer per project conventions.
- Preserve the existing HTMX partial-update UX — all filter changes trigger seamless `#event-results` replacement.
- Maintain progressive enhancement: filters work as standard GET parameters if JavaScript is disabled.
- Keep existing URL patterns, API field names, and `q` parameter intact.

**Non-Goals:**

- Full-text search or search ranking (simple `icontains` suffices).
- Pagination changes (existing pagination, if any, continues to work with filtered querysets — but pagination itself is not being added or redesigned here).
- Server-side form validation with error feedback (filters silently degrade: invalid date values are ignored, missing params return unfiltered results).
- Location geocoding or radius-based search.
- Saved searches or filter presets.

## Decisions

### 1. Selector function signature

**Decision**: `get_events(*, query: str | None, category_id: int | None, date_from: date | None, date_to: date | None, location: str | None) → QuerySet[Event]`

**Rationale**: Keyword-only arguments prevent accidental positional misuse. Returns a QuerySet (not a list) to allow downstream chaining (e.g., pagination, ordering). Each filter is independently optional — `None` means "don't filter on this criterion."

**Alternatives considered**:
- Pass a dict or dataclass → more ceremony with no benefit for 5 parameters.
- Accept raw strings and parse inside selector → violates separation of concerns; view should validate/parse before calling selector.

### 2. Date filtering semantics

**Decision**: `date_from` and `date_to` filter on the `date` field using `date__date__gte` and `date__date__lte` (date-only comparison, ignoring time component).

**Rationale**: The HTML `<input type="date">` returns `YYYY-MM-DD` without time. Users expect "events on July 27" to match regardless of event start time. Using `__date` lookup extracts the date portion of the DateTimeField for comparison.

**Alternatives considered**:
- Compare against full datetime → confusing UX ("I selected July 27 but the 10pm event is missing because I didn't set time").
- Convert to datetime at start/end of day → more complex, same result.

### 3. HTMX multi-input coordination

**Decision**: Wrap all filter inputs in a single `<form>` and use `hx-include="closest form"` (or rely on the form's `hx-get`) so that every input change sends ALL current filter values.

**Rationale**: Without `hx-include`, each HTMX-triggered input would only send its own value, losing the state of other filters. The existing search input already lives in a `<form>`, so extending it with more inputs is natural. Each input gets `hx-get` + `hx-trigger="change"` (or `"input changed delay:300ms"` for text fields) + `hx-target="#event-results"`.

**Issue #15 critique**: The Issue suggests `hx-trigger="change, input changed delay:300ms"` on all inputs. This is partially wrong:
- For `<select>` and `<input type="date">`, `change` alone is correct (no debounce needed — user makes a discrete selection).
- For text inputs (`q`, `location`), `input changed delay:300ms` with debounce is correct (avoids excessive requests while typing).
- Using both `change` AND `input changed delay:300ms` on text inputs causes duplicate requests (one on `change` blur, one on debounced `input`).

**Decision**: Use `hx-trigger="input changed delay:300ms"` for text inputs, `hx-trigger="change"` for select/date inputs.

### 4. Category context passing

**Decision**: The `event_list` view always passes `categories` (all Category objects) in the template context, regardless of whether the request is an HTMX partial or full page.

**Rationale**: For full-page loads, the category dropdown needs the list. For HTMX partial responses, the category list is not rendered (only `_event_results.html` is returned), so the extra context is harmless overhead — a single `Category.objects.all()` query on a small table.

**Issue #15 critique**: The Issue says "Pass available categories and current filter states in the template context" but doesn't mention that for HTMX requests, only the partial template is rendered so the filter controls are never re-rendered. The current filter state in context is useful for the full-page (non-HTMX) case to pre-fill inputs, but for HTMX partial updates the client-side form already holds state. We'll pass `categories` and current filter values in context for the full-page case only; the HTMX partial just needs the filtered `events`.

### 5. Location filtering: `icontains`

**Decision**: Use `location__icontains` for location filtering, same as title search.

**Rationale**: Consistent with the existing search approach. Exact match would be too strict for partial input (e.g., "Tokyo" should match "Tokyo, Shibuya").

## Risks / Trade-offs

- **[No DB index on `location`]** → Acceptable for a small local-events app. If performance becomes an issue, add `db_index=True` to the `location` field.
- **[Category dropdown could grow large]** → Mitigated by the fact that categories in this app are admin-managed and expected to remain small. If user-created categories are added later, consider a searchable select widget.
- **[HTMX partial updates don't update the URL bar]** → Users cannot bookmark filtered results. Mitigated by progressive enhancement: the form also works as a standard GET submission. Could add `hx-push-url="true"` later if needed.
- **[Date input browser support]** → `<input type="date">` is well-supported in modern browsers. Older browsers fall back to a text input; the view should handle gracefully by ignoring unparseable date strings.
