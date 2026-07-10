## Why

The project currently has Django models (Event, Category) and a configured project, but no view functions or URL routing beyond the admin site. Users cannot interact with the application through a browser. This change introduces the first set of basic view functions to turn the project into a working web application, covering essential user actions like viewing the home page, browsing events, and viewing event details.

## What Changes

- Add view functions to `apps/events/views.py` for core user actions:
  - Home page view (landing page)
  - Event list view (browse all events)
  - Event detail view (view a single event)
  - Event create form view (display the creation form)
  - Event create handler (process form submission, with some hard-coded values for now)
- Create `apps/events/urls.py` with URL patterns for the events app
- Update `config/urls.py` to include the events app URLs
- Update project documentation (README, OpenSpec specs) to reflect the callable URLs, their arguments, and return values

## Capabilities

### New Capabilities
- `basic-views`: View functions and URL routing for the events app, covering home page, event listing, event detail, and event creation (initial/stub versions)

### Modified Capabilities
- `core-project`: Adding URL routing configuration to connect views to the project

## Impact

- **Code**: `apps/events/views.py`, `apps/events/urls.py` (new), `config/urls.py`
- **APIs**: New callable URLs at `/`, `/events/`, `/events/<id>/`, `/events/create/`
- **Dependencies**: No new dependencies required; uses Django's built-in `HttpResponse` and `JsonResponse`
- **Documentation**: README.md and OpenSpec specs to be updated with URL API documentation
