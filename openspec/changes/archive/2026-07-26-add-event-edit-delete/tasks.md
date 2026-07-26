## 1. Service Layer Implementation

- [x] 1.1 Implement `update_event(event, **kwargs)` function in `apps/events/services.py` to handle event updates
- [x] 1.2 Implement `delete_event(event)` function in `apps/events/services.py` to handle event removal

## 2. Views and URL Routing

- [x] 2.1 Implement `event_edit` view in `apps/events/views.py` handling both GET (pre-populated form) and POST (update submission with authorization check)
- [x] 2.2 Implement `event_delete` view in `apps/events/views.py` handling POST requests with authorization check
- [x] 2.3 Map `/events/<int:event_id>/edit/` and `/events/<int:event_id>/delete/` routes in `apps/events/urls.py`

## 3. Templates and UI Integration

- [x] 3.1 Create `apps/events/templates/events/event_edit.html` with form fields matching `event_create.html` pre-filled with event data
- [x] 3.2 Update `apps/events/templates/events/event_detail.html` to add conditional "Edit" and "Delete" buttons visible only to authorized creators or administrators

## 4. Documentation Update

- [x] 4.1 Update `README.md` to add an "Unimplemented Features" (未実装の機能) section documenting filtering by date/category/location, pagination, calendar widgets, submit protection, and optional favorites

## 5. Verification and Testing

- [x] 5.1 Add automated unit tests in `apps/events/tests.py` verifying that event creators and administrators can successfully edit and delete events
- [x] 5.2 Add automated unit tests in `apps/events/tests.py` verifying that unauthorized users receive a 403 Forbidden or redirection when attempting to edit or delete events
- [x] 5.3 Run all tests (`pytest`) and linter (`ruff check`) to verify project stability
