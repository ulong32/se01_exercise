# event-edit-delete Specification

## Purpose
TBD - Specifications for event editing and deletion workflows with creator/admin authorization controls.

## Requirements

### Requirement: Event Edit Form View
The system SHALL provide a view at `/events/<id>/edit/` that responds to GET requests by rendering an HTML form pre-populated with the target event's current details. Only the original creator of the event or a system administrator (superuser or staff) SHALL be permitted to access this view.

#### Scenario: Creator accesses edit form
- **WHEN** an authenticated user who is the creator of the event sends a GET request to `/events/<id>/edit/`
- **THEN** the system returns an HTTP 200 response containing the edit form populated with the event's title, description, date, location, and category

#### Scenario: Administrator accesses edit form
- **WHEN** an authenticated user who is a superuser or staff member sends a GET request to `/events/<id>/edit/`
- **THEN** the system returns an HTTP 200 response containing the edit form populated with the event's current details

#### Scenario: Unauthorized user accesses edit form
- **WHEN** an authenticated user who is neither the creator nor an administrator sends a GET request to `/events/<id>/edit/`
- **THEN** the system returns an HTTP 403 Forbidden response or redirects the user with an error message

#### Scenario: Unauthenticated user accesses edit form
- **WHEN** an unauthenticated user sends a GET request to `/events/<id>/edit/`
- **THEN** the system redirects the user to the login page

### Requirement: Event Update Handler
The system SHALL provide a handler at `/events/<id>/edit/` that processes POST requests to update an existing event. It MUST validate all required fields and verify that the requesting user is the creator or an administrator before modifying the database.

#### Scenario: Successful event update by creator
- **WHEN** the event creator submits a valid POST request to `/events/<id>/edit/`
- **THEN** the system updates the event in the database and redirects to `/events/<id>/`

#### Scenario: Unauthorized update attempt
- **WHEN** a user who is neither the creator nor an administrator submits a POST request to `/events/<id>/edit/`
- **THEN** the system does not modify the event and returns an HTTP 403 Forbidden response

### Requirement: Event Deletion Handler
The system SHALL provide a handler at `/events/<id>/delete/` that processes POST requests to delete an event. It MUST verify that the requesting user is the creator or an administrator before deleting the event from the database.

#### Scenario: Successful deletion by creator
- **WHEN** the event creator submits a POST request to `/events/<id>/delete/` with a valid CSRF token
- **THEN** the system deletes the event from the database and redirects to `/events/`

#### Scenario: Unauthorized deletion attempt
- **WHEN** a user who is neither the creator nor an administrator submits a POST request to `/events/<id>/delete/`
- **THEN** the system does not delete the event and returns an HTTP 403 Forbidden response

### Requirement: Conditional UI Action Buttons
The system SHALL display "Edit" and "Delete" action links or buttons on the event detail view (`/events/<id>/`) only when the currently authenticated user is authorized to modify the event.

#### Scenario: Action buttons shown to creator
- **WHEN** the event detail page is rendered for the event creator
- **THEN** the HTML includes links/buttons to edit and delete the event

#### Scenario: Action buttons hidden from unauthorized user
- **WHEN** the event detail page is rendered for an unauthenticated user or an authenticated user who is not the creator or an administrator
- **THEN** the HTML does not include links or buttons to edit or delete the event
