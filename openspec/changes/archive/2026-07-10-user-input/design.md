## Context

Currently, the web application relies on hardcoded stubs for viewing and creating content. To become a functional application, it needs to accept, validate, and process real user input. This design outlines the approach for adding HTML forms and transitioning views from stubs to actual data processing handlers.

## Goals / Non-Goals

**Goals:**
- Replace placeholder views with functional GET and POST handlers.
- Introduce HTML forms for submitting data to the server.
- Define what data should be submitted, its HTTP method, and basic validation requirements.
- Update templates to include `<form>` elements and CSRF tokens.

**Non-Goals:**
- Advanced client-side JavaScript validation (focus is on HTML5 attributes like `required`).
- Complex custom form widgets or styling (the focus is on functional wiring and primitive HTML pages).

## Decisions

**1. Form Submission Methods (GET vs POST)**
- **Decision:** Forms that query or filter data (like search) will use `GET`. Forms that create, update, or delete records (like event creation) will use `POST`.
- **Rationale:** This follows REST semantics. GET requests should be idempotent, while POST requests should be used for state-changing operations.

**2. Form Validation Approach**
- **Decision:** Basic validation will be enforced server-side by checking the presence of required fields in `request.POST` or `request.GET`. Client-side validation will rely on HTML5 `required`, `type="date"`, etc.
- **Rationale:** Server-side validation is mandatory for data integrity. HTML5 attributes provide a standardized, lightweight user experience enhancement without requiring custom JS.

**3. Security and State Management**
- **Decision:** All POST forms must include Django's `{% csrf_token %}` template tag. After successful POST operations, the server will issue an HTTP 302 Redirect to a GET endpoint.
- **Rationale:** CSRF tokens prevent Cross-Site Request Forgery. The Post-Redirect-Get (PRG) pattern prevents duplicate form submissions if a user refreshes the page.

**4. User Creation**
- **Decision:** A User Registration form and handler will be added. This is required because creating an Event requires a `creator` (User).
- **Rationale:** The system cannot create valid events without existing users. Providing a simple user creation form enables the event creation flow to work end-to-end.

## Risks / Trade-offs

- **[Risk] Missing CSRF Token** → **Mitigation**: Django's middleware will return a 403 Forbidden. Ensure all POST templates include `{% csrf_token %}`.
- **[Risk] Invalid Data Saving** → **Mitigation**: Server-side checks must happen before creating database records to prevent database constraint errors.
