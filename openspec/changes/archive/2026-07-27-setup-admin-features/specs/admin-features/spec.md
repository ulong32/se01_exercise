## ADDED Requirements

### Requirement: Event Model Admin Registration
The system SHALL register the `Event` model in the Django admin interface with configured list display, filtering, search capabilities, and optimized foreign key lookups.

#### Scenario: Admin views event list
- **WHEN** an authenticated administrator accesses the Event list in the Django admin interface
- **THEN** the system displays events with columns for title, category, date, location, and creator, and provides filter options for category and date.

#### Scenario: Admin searches events
- **WHEN** an administrator submits a search query in the Event admin search bar
- **THEN** the system filters the displayed events by matching the query against event title, description, or location.

### Requirement: Category Model Admin Registration
The system SHALL register the `Category` model in the Django admin interface with search capabilities.

#### Scenario: Admin views category list
- **WHEN** an authenticated administrator accesses the Category list in the Django admin interface
- **THEN** the system displays the list of categories and provides a search bar to search categories by name.

### Requirement: Admin User Setup Command
The system SHALL provide a management command (`setup_admin`) to idempotently create or verify an administrative superuser account based on environment configuration or safe defaults.

#### Scenario: Executing setup admin command when user does not exist
- **WHEN** the `setup_admin` management command is executed and the configured admin user does not exist
- **THEN** the system creates a new superuser account with administrative privileges and outputs a success confirmation.

#### Scenario: Executing setup admin command when user already exists
- **WHEN** the `setup_admin` management command is executed and the configured admin user already exists
- **THEN** the system leaves the existing account intact without errors and outputs a message indicating the user already exists.
