# User Input Constraints

## Purpose
Defines constraints and patterns for handling user input via HTML forms, including validation, CSRF protection, and Post-Redirect-Get.

## Requirements

### Requirement: User Input Forms
The system SHALL provide HTML forms for users to input data. Forms that retrieve or filter data MUST use the GET method, while forms that mutate state (create, update, delete) MUST use the POST method.

#### Scenario: Submitting a search query
- **WHEN** user submits a search or filter form
- **THEN** the browser sends a GET request with form data in the query string

#### Scenario: Submitting a creation form
- **WHEN** user submits a form to create a new entity
- **THEN** the browser sends a POST request with form data in the request body

### Requirement: Form Validation
The system SHALL validate submitted form data before processing. Required fields MUST be checked for presence. If validation fails, the system MUST return a 400 Bad Request or re-render the form indicating errors.

#### Scenario: Valid form submission
- **WHEN** user submits a POST form with all required fields present
- **THEN** the server processes the data successfully

#### Scenario: Invalid form submission
- **WHEN** user submits a POST form missing a required field
- **THEN** the server rejects the submission and returns a 400 response or error page

### Requirement: CSRF Protection
The system SHALL protect all POST forms from Cross-Site Request Forgery by including a CSRF token.

#### Scenario: Submitting POST without CSRF token
- **WHEN** user submits a POST request without a valid CSRF token
- **THEN** the system returns a 403 Forbidden response

### Requirement: Post-Redirect-Get (PRG) Pattern
The system SHALL redirect the user to a success page or another appropriate GET endpoint after successfully processing a state-mutating POST request to prevent duplicate submissions.

#### Scenario: Successful POST submission
- **WHEN** user successfully submits a POST form (e.g., creating an event)
- **THEN** the server responds with an HTTP 302 Redirect to a relevant view page
