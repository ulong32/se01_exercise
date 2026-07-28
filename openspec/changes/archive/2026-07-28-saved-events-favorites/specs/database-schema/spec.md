## ADDED Requirements

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
