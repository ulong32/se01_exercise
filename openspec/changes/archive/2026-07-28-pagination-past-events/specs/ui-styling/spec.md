## ADDED Requirements

### Requirement: Past Event Visual Styling
The system SHALL define a CSS class `.past-event` in `static/css/styles.css` that visually distinguishes past events from upcoming events. The class SHALL apply `opacity: 0.6` and `filter: grayscale(60%)` to reduce visual prominence. The `.past-event` class SHALL reduce or disable hover effects (no `translateY` transform on hover). A transition SHALL be applied so the gray-out effect is smooth.

#### Scenario: Past event card appears grayed out
- **WHEN** an event card has the `.past-event` class applied
- **THEN** the card is rendered with reduced opacity (0.6) and a grayscale filter (60%), making it visually distinct from upcoming events

#### Scenario: Past event card hover effect is muted
- **WHEN** user hovers over an event card with the `.past-event` class
- **THEN** the card does not lift (no `translateY` transform) and the hover glow effect is suppressed

### Requirement: Pagination Navigation Styling
The system SHALL define CSS styles for pagination navigation in `static/css/styles.css`. The pagination component SHALL use a horizontal flexbox layout with centered alignment. Page number links SHALL be styled as pill-shaped buttons. The current/active page SHALL be visually highlighted using the accent gradient. Previous/Next links SHALL be styled consistently with page number links. Disabled Previous/Next links (on first/last page) SHALL appear muted.

#### Scenario: Pagination navigation is horizontally centered
- **WHEN** the pagination navigation is rendered below the event grid
- **THEN** the navigation links are displayed in a centered horizontal row with consistent spacing

#### Scenario: Active page is visually highlighted
- **WHEN** the pagination navigation is rendered and the user is on page 2
- **THEN** the page 2 link is styled with the accent gradient background and white text, distinguishing it from other page links

#### Scenario: Disabled navigation link appears muted
- **WHEN** the user is on the first page of results
- **THEN** the "Previous" link is styled with reduced opacity and is not clickable
