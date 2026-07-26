## Why

The application currently allows users to create events, but lacks functionality to edit or delete them once created. Enabling event modification and removal is essential for event lifecycle management, and access must be securely restricted to the original event creator or system administrators. Additionally, several features described in `README.md` (such as date/location/category filtering, pagination, and visual calendar widgets) are not yet implemented; updating the README to explicitly document these as unimplemented ensures project clarity and alignment between documentation and codebase.

## What Changes

- Add an event edit page (`/events/<id>/edit/`) with a pre-filled form for updating existing event details.
- Add an event update handler that validates input and updates the event in the database if the requesting user is authorized.
- Add an event delete handler (`/events/<id>/delete/`) that removes an event if the requesting user is authorized.
- Implement authorization checks ensuring only the original event creator or a superuser/admin can edit or delete an event.
- Add Edit and Delete buttons to the event detail template (`event_detail.html`), visible only to authorized users.
- Update `README.md` to add an "Unimplemented Features" (未実装の機能) section clarifying which features mentioned in the overview are out of scope for current implementation (e.g., date/category/location filtering, pagination, calendar widgets, submit protection, and optional favorites table).

## Capabilities

### New Capabilities
- `event-edit-delete`: Covers event modification and deletion workflows, including form views, POST handlers, and authorization rules restricting edit and delete operations to the event creator or system administrators.

### Modified Capabilities
- `core-project`: Document unimplemented features in `README.md` to maintain accurate project-level documentation.

## Impact

- **Views & Routing**: Adds `event_edit` and `event_delete` views in `apps/events/views.py` and maps them in `apps/events/urls.py`.
- **Services**: Adds `update_event` and `delete_event` service functions in `apps/events/services.py` following project architecture conventions.
- **Templates**: Creates `apps/events/templates/events/event_edit.html` and modifies `apps/events/templates/events/event_detail.html` to include action buttons.
- **Documentation**: Updates `README.md` to explicitly list remaining unimplemented features.
