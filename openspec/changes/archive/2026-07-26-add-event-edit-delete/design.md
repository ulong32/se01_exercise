## Context

The event listings application currently supports event creation (`/events/create/`), listing (`/events/`), and detail viewing (`/events/<id>/`), but does not allow event modification or deletion. Furthermore, the existing project documentation in `README.md` mentions advanced features such as date/location/category filtering, pagination, calendar widgets, and submit protection, none of which are currently implemented in the codebase. To maintain code quality and secure domain operations without introducing regression or scope creep, we need to implement edit and delete workflows for events with strict authorization controls, while simultaneously updating `README.md` to clarify the actual status of unimplemented features.

## Goals / Non-Goals

**Goals:**
- Provide an event editing form view at `/events/<id>/edit/` that pre-populates existing event data and updates the event via POST.
- Provide an event deletion view/handler at `/events/<id>/delete/` that removes an event from the database via POST (or GET confirmation form).
- Enforce strict authorization in both views and services: only the user who created the event (`event.creator == request.user`) or a system administrator (`request.user.is_superuser` or `is_staff`) may edit or delete it.
- Update `event_detail.html` to conditionally display "Edit" and "Delete" buttons for authorized users.
- Add an explicit "Unimplemented Features" (未実装の機能) section to `README.md` listing out-of-scope features (filtering by date/category/location, pagination, calendar widgets, submit protection, and favorites).

**Non-Goals:**
- Implementing the missing search filters (date, category, location) in this change.
- Implementing pagination or past event graying/hiding in this change.
- Implementing visual calendar widgets or submit-protection tokens in this change.
- Implementing the optional `favorites` junction table in this change.

## Decisions

### 1. Service Layer Pattern for Update and Delete
- **Decision:** Implement `update_event(event, **kwargs)` and `delete_event(event)` functions in `apps/events/services.py` rather than placing ORM modification logic directly inside views or forms.
- **Rationale:** Aligns with project conventions in `AGENTS.md` ("Put business workflow logic in `services.py`, not in views or serializers").
- **Alternatives Considered:** Updating and deleting model instances directly in `views.py`. This was rejected because it violates project architectural guidelines.

### 2. Authorization Check Strategy
- **Decision:** Perform authorization checks both in the view layer (to return HTTP 403 Forbidden or redirect if unauthorized) and in the template layer (`{% if request.user == event.creator or request.user.is_superuser or request.user.is_staff %}`) to hide action buttons from unauthorized users.
- **Rationale:** Preventing unauthorized users from seeing action buttons improves UX, while backend validation in view handlers ensures security against direct URL access.

### 3. README Documentation Strategy
- **Decision:** Add a dedicated subsection `## Unimplemented Features (未実装機能)` in `README.md` directly under Core Features to explicitly list features described in the project scope that are not yet built.
- **Rationale:** Aligns with user instructions to clarify project scope without removing the original feature descriptions, ensuring transparency for future contributors.

## Risks / Trade-offs

- **Risk: Unauthorized Modification / Deletion**
  → *Mitigation:* Ensure unit tests specifically test that normal users cannot edit or delete events created by other users, asserting HTTP 403 or redirect responses.
- **Risk: CSRF Vulnerability on Deletion**
  → *Mitigation:* Ensure deletion requires a POST request protected by a `{% csrf_token %}` rather than a simple GET link.
