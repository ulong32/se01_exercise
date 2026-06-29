## ADDED Requirements

### Requirement: Event Model Definition
The system SHALL define an Event model containing fields for title, description, date, location, category, and creator.

#### Scenario: Instantiating an event
- **WHEN** user provides valid data for title, description, date, location, category, and creator
- **THEN** an Event object is successfully created and saved in the database

### Requirement: Category Model Definition
The system SHALL define a Category model with a name field.

#### Scenario: Creating a category
- **WHEN** user provides a valid name string
- **THEN** a Category object is successfully created in the database

### Requirement: Admin String Representation
The system SHALL implement `__str__` methods for Event and Category models to facilitate administrative viewing.

#### Scenario: Viewing model instances as strings
- **WHEN** `str(Event)` or `str(Category)` is called
- **THEN** it returns a human-readable identifier (like the title or name)
