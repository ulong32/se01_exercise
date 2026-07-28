# submit-protection Specification

## Requirements

### Requirement: Frontend Submit Button Protection
The system SHALL disable the submit button immediately upon form submission for all forms marked with the `data-submit-protect` attribute. While the submission is in progress, the button text SHALL change to a loading message (e.g., "Submitting…") and the button SHALL be visually styled with the `.is-submitting` CSS class to indicate processing.

#### Scenario: User clicks submit on a protected form
- **WHEN** user clicks the submit button on a form with `data-submit-protect` attribute
- **THEN** the submit button is immediately disabled and its text changes to "Submitting…"

#### Scenario: User attempts to double-click submit
- **WHEN** user rapidly clicks the submit button multiple times on a protected form
- **THEN** only the first click triggers form submission; subsequent clicks are ignored because the button is already disabled

### Requirement: Backend Time-Window Deduplication for Event Creation
The system SHALL reject duplicate event creation requests from the same user when an event with identical `title`, `creator`, and `date` was created within the last 5 seconds. Instead of creating a duplicate, the system SHALL return the previously created event.

#### Scenario: Duplicate event creation within time window
- **WHEN** a user submits an event creation request with title, creator, and date matching an event created by the same user within the last 5 seconds
- **THEN** the system returns the existing event without creating a duplicate

#### Scenario: Legitimate event creation outside time window
- **WHEN** a user submits an event creation request and no matching event exists within the 5-second window
- **THEN** the system creates and returns a new event normally

#### Scenario: Same title different creator
- **WHEN** two different users submit event creation requests with the same title and date within 5 seconds
- **THEN** the system creates separate events for each user

### Requirement: Event Model Created-At Timestamp
The system SHALL store a `created_at` timestamp on every Event record, automatically set to the current time when the event is created. This field SHALL be used for time-window deduplication queries.

#### Scenario: Event creation records timestamp
- **WHEN** a new event is created
- **THEN** the `created_at` field is automatically set to the current datetime
