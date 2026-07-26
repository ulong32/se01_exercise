## ADDED Requirements

### Requirement: Django Project Initialization
The system SHALL have a valid Django project wrapper configured with URL routing that includes both the admin site and the events application URLs.

#### Scenario: Running the dev server
- **WHEN** user runs `python manage.py runserver`
- **THEN** the local development server starts without configuration errors

#### Scenario: Accessing app URLs
- **WHEN** user navigates to any URL defined in the events app
- **THEN** the request is routed correctly through `config/urls.py` to the events app URL configuration

### Requirement: Event Application Setup
The system SHALL have an app named `events` registered in the project's installed apps.

#### Scenario: Running migrations
- **WHEN** user runs `python manage.py makemigrations` and `migrate`
- **THEN** it correctly creates the tables for the events app without errors

### Requirement: Unimplemented Features Documentation
The system documentation in `README.md` SHALL include an explicit subsection outlining which features described in the general overview remain unimplemented in the current codebase. This ensures consistency between project scope descriptions and actual implementation status.

#### Scenario: Reviewing README documentation
- **WHEN** a developer or user reads `README.md`
- **THEN** they find an explicit list of unimplemented features (including date/category/location filtering, pagination, calendar widgets, submit protection, and optional favorites table)
