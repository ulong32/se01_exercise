## Why

The event listing view (`/events/`) currently fetches all events from the database at once with no pagination, which degrades performance and user experience as the dataset grows. Additionally, there is no mechanism to distinguish past events from upcoming ones—users have to manually scan dates to find events that are still relevant.

## What Changes

- **Add server-side pagination** to the event list view using Django's `Paginator`, defaulting to 12 events per page.
- **Integrate pagination with HTMX**: Pagination navigation controls (Previous/Next, page numbers) will trigger partial page updates via HTMX attributes, preserving all active filter/search parameters across page transitions.
- **Add past-event filtering and visual distinction**: Events whose date has passed will receive a `.past-event` CSS class for gray-out styling. A new "Include past events" checkbox will allow users to toggle visibility of past events (hidden by default).
- **Extend the selector** (`get_events()`) with an `include_past` parameter to optionally exclude past events from the queryset.
- **Update the event results partial template** (`_event_results.html`) to include pagination navigation and past-event CSS classes.

## Capabilities

### New Capabilities

_(none — all changes extend existing capabilities)_

### Modified Capabilities

- `basic-views`: Adding pagination to the Event List View requirement and adding a new "Past Events Control" requirement covering the `include_past` filter, `is_past` annotation, and updated selector signature.
- `htmx-dynamic-search`: Pagination navigation controls must trigger HTMX partial updates and preserve all active filters across paginated requests. The "Include past events" checkbox must also integrate with the existing HTMX filter flow.
- `ui-styling`: Adding `.past-event` visual gray-out styles and pagination navigation component styles.

## Impact

- **`apps/events/selectors.py`**: New `include_past` kwarg and `is_past` annotation on the queryset.
- **`apps/events/views.py`**: Integration of `Paginator`, passing the `Page` object and pagination metadata to the template context.
- **`apps/events/templates/events/_event_results.html`**: New pagination nav, `.past-event` class on event cards, and HTMX attributes on pagination links.
- **`apps/events/templates/events/event_list.html`**: New "Include past events" toggle checkbox with HTMX attributes.
- **`static/css/styles.css`**: New `.past-event` and pagination nav styles.
- **`openspec/specs/basic-views/spec.md`**: Spec updates for pagination and past events requirements.
- **Tests**: New test coverage for pagination behavior, filter+pagination combined scenarios, and past-event classification.
