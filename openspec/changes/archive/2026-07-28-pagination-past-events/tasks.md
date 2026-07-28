## 1. Selector: Past Events Filtering

- [x] 1.1 Add `include_past: bool = False` keyword argument to `get_events()` in `apps/events/selectors.py`
- [x] 1.2 When `include_past` is `False`, filter the queryset with `date__gte=timezone.now()` to exclude past events
- [x] 1.3 Verify existing filter logic (query, category_id, date_from, date_to, location) still works correctly with the new parameter

## 2. View: Pagination & Past Events Integration

- [x] 2.1 Import `Paginator` and `EmptyPage`/`PageNotAnInteger` from `django.core.paginator` in `apps/events/views.py`
- [x] 2.2 Parse the `include_past` GET parameter (checkbox value `"true"`) and pass it to `get_events()`
- [x] 2.3 Parse the `page` GET parameter and apply `Paginator` (page_size=12) to the filtered queryset
- [x] 2.4 Handle invalid/out-of-range page numbers by falling back to page 1
- [x] 2.5 Pass `page_obj`, `include_past` (string value for checkbox state), and `now` (timezone-aware) to the template context
- [x] 2.6 Update the HTMX branch to also paginate and include `page_obj` and `now` in the partial response context

## 3. Template: Pagination Navigation & Past Event Styling

- [x] 3.1 Update `_event_results.html`: iterate over `page_obj` instead of `events`, add `.past-event` class to `<article>` when `event.date < now`
- [x] 3.2 Add pagination navigation block below the event list in `_event_results.html` with Previous/Next and page number links using HTMX attributes (`hx-get`, `hx-target`, `hx-swap`, `hx-include`)
- [x] 3.3 Add "Include past events" checkbox to the search form in `event_list.html` with HTMX attributes (`hx-trigger="change"`, `hx-include="closest form"`) and preserve checked state from context

## 4. CSS: Past Event & Pagination Styles

- [x] 4.1 Add `.past-event` styles in `static/css/styles.css`: `opacity: 0.6`, `filter: grayscale(60%)`, muted hover effects
- [x] 4.2 Add `.pagination` navigation styles: centered flexbox layout, pill-shaped page links, accent-gradient active state, muted disabled state

## 5. Spec Documentation

- [x] 5.1 Verify delta specs in `openspec/changes/pagination-past-events/specs/` match the final implementation

## 6. Tests

- [x] 6.1 Add test: default event list excludes past events
- [x] 6.2 Add test: `include_past=true` shows all events including past
- [x] 6.3 Add test: pagination returns correct page of results (page 1 vs page 2)
- [x] 6.4 Add test: invalid page number falls back to page 1
- [x] 6.5 Add test: pagination combined with filters returns correct filtered+paginated results
- [x] 6.6 Add test: HTMX request with pagination returns partial HTML with pagination controls
- [x] 6.7 Add test: `get_events(include_past=False)` excludes past events at the selector level
- [x] 6.8 Add test: `get_events(include_past=True)` includes past events at the selector level
