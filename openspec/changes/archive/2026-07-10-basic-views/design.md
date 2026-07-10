## Context

The project has a functional Django setup with `Event` and `Category` models, migrations applied, and an admin site. However, the only accessible URL is `/admin/`. There are no view functions, no app-level URL routing, and no way for end users to interact with the application through a browser. The `apps/events/views.py` is empty.

Current state:
- Models: `Event` (title, description, date, location, category FK, creator FK), `Category` (name)
- URL routing: Only `admin/` in `config/urls.py`
- Views: None
- Templates: None (views will return `HttpResponse` / `JsonResponse` for now)

## Goals / Non-Goals

**Goals:**
- Create basic view functions for the events app that represent clear user actions
- Wire up URL routing at both app level (`apps/events/urls.py`) and project level (`config/urls.py`)
- Return simple `HttpResponse` / `JsonResponse` responses (no templates required yet)
- Document the URL API (endpoints, arguments, return values)
- Some user-supplied values may be hard-coded for now (e.g., creator ID in event creation)

**Non-Goals:**
- Full HTML templates or styled UI (views will return plain text / JSON for now)
- User authentication or permission enforcement
- Form validation beyond basic required fields
- Dynamic search or filtering
- Pagination
- Template rendering system

## Decisions

### Decision 1: Function-based views (FBV) over class-based views (CBV)

**Choice**: Use function-based views.
**Rationale**: The exercise goal is to create simple, clear view functions. FBVs are easier to understand, more explicit, and appropriate for the initial stage. CBVs can be introduced later when views grow in complexity.
**Alternative considered**: CBVs with `ListView`, `DetailView` — overkill for stub views that return `HttpResponse`.

### Decision 2: Use `HttpResponse` and `JsonResponse` (no templates yet)

**Choice**: Return plain `HttpResponse` for page views and `JsonResponse` for data endpoints.
**Rationale**: Templates are not the focus of this exercise. Simple responses keep the change minimal and testable. This aligns with the exercise note that "views do not need to be complete yet."
**Alternative considered**: Minimal template rendering — adds unnecessary complexity at this stage.

### Decision 3: App-level `urls.py` with `include()` in project URLs

**Choice**: Create `apps/events/urls.py` and include it from `config/urls.py` using `include()`.
**Rationale**: Django best practice for app modularity. Keeps event-related URLs self-contained and makes future changes easier.
**Alternative considered**: All URLs in `config/urls.py` — poor separation of concerns.

### Decision 4: Hard-code creator for event creation

**Choice**: Use `User.objects.first()` or a fixed user lookup for the creator field in the create view.
**Rationale**: Authentication is not implemented yet. The exercise explicitly allows hard-coded values. This keeps the view functional without requiring login.
**Alternative considered**: Skip create functionality entirely — loses a valuable exercise objective.

### Decision 5: View function set

The following five views cover the core user actions:

| View Function | URL Pattern | HTTP Method | Description |
|---|---|---|---|
| `home` | `/` | GET | Landing page, welcome message |
| `event_list` | `/events/` | GET | List all events |
| `event_detail` | `/events/<int:event_id>/` | GET | Show single event details |
| `event_create` | `/events/create/` | GET | Show event creation form (stub) |
| `event_create` | `/events/create/` | POST | Process event creation |

## Risks / Trade-offs

- **[Hard-coded creator]** → Will need refactoring when authentication is added. Mitigation: Document this clearly as a temporary measure; keep the hard-coded logic isolated.
- **[No input validation]** → POST handler has minimal validation. Mitigation: Acceptable for this exercise stage; full form validation will come with Django Forms.
- **[No CSRF protection on POST]** → Using `@csrf_exempt` for the create POST since there's no template/form rendering. Mitigation: This is temporary; proper CSRF handling will come with template-based forms.
- **[Plain text responses]** → Not user-friendly. Mitigation: Templates will replace these in a future change.
