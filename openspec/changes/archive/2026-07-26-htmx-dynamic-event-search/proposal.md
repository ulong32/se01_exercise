## Why

The current event search on the event list page (`/events/`) performs a full-page reload on every search submission. This creates a sluggish user experience—the entire page re-renders (header, footer, CSS re-parse) just to update the event results. Introducing HTMX-powered dynamic search allows the event list to update instantly as the user types or submits, without a full-page reload, resulting in a faster and more modern interaction.

## What Changes

- Add HTMX library to the base template so all pages can leverage it.
- Convert the event search on the event list page to a dynamic, HTMX-driven interaction:
  - Typing in the search input (with debounce) triggers an HTTP GET request.
  - Only the event results area is swapped with the server response (partial HTML fragment).
- Add a new Django view (or modify the existing `event_list` view) that returns a **partial HTML fragment** (just the event cards list) when the request is an HTMX request, and the full page otherwise.
- Add a partial template for the event results fragment (`_event_results.html`).

## Capabilities

### New Capabilities
- `htmx-dynamic-search`: HTMX-based dynamic event search that updates the event list without full-page reloads, including the server-side partial response endpoint and the client-side HTMX integration.

### Modified Capabilities
- `basic-views`: The event list view gains HTMX-aware partial rendering behavior—returning only the event results fragment for HTMX requests instead of the full page.

## Impact

- **Templates**: `base.html` gains an HTMX `<script>` tag; `event_list.html` gains `hx-get`, `hx-trigger`, `hx-target` attributes on the search input; new `_event_results.html` partial template.
- **Views**: `apps/events/views.py` `event_list` view updated to detect HTMX requests and return partial HTML.
- **Dependencies**: HTMX library added (CDN script tag, no Python dependency).
- **No database or model changes required.**
- **No API field or URL name changes.**
