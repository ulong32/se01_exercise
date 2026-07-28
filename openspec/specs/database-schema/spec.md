# database-schema Specification

## Purpose
Defines the core database models, schema structures, and administrative representations for the application.
## Requirements
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

### Requirement: Favorite Junction Model Definition
The system SHALL define a `Favorite` junction model containing a `user` ForeignKey to `settings.AUTH_USER_MODEL` (on_delete=CASCADE), an `event` ForeignKey to `Event` (on_delete=CASCADE), and a `created_at` DateTimeField with `auto_now_add=True`. The model SHALL enforce `unique_together = ("user", "event")` to prevent duplicate bookmarks.

#### Scenario: Instantiating a favorite
- **WHEN** a valid user and event are provided
- **THEN** a Favorite object is successfully created in the database with an auto-populated `created_at` timestamp

#### Scenario: Duplicate favorite prevention
- **WHEN** a user attempts to create a second Favorite for the same event
- **THEN** the database raises an IntegrityError

#### Scenario: Favorite string representation
- **WHEN** `str(Favorite)` is called
- **THEN** it returns a human-readable identifier (e.g., "username → event title")

