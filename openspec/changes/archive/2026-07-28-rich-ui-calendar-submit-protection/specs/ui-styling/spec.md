## ADDED Requirements

### Requirement: Flatpickr Calendar Widget Styling
The system SHALL load Flatpickr's CSS from a CDN link in the base template `<head>`. Any project-specific overrides to Flatpickr's appearance SHALL be defined in `static/css/styles.css` using class selectors. No inline `style="..."` attributes SHALL be used for Flatpickr customisation.

#### Scenario: Flatpickr CSS is loaded via CDN
- **WHEN** any page is rendered
- **THEN** the HTML `<head>` contains a `<link>` element referencing Flatpickr's CSS from a CDN

#### Scenario: Flatpickr overrides use external CSS
- **WHEN** Flatpickr styling is customised for the project
- **THEN** override rules are defined in `static/css/styles.css`, not via inline styles

### Requirement: Submit Button Loading State Styling
The system SHALL style the submit button's loading state using the `.is-submitting` CSS class in `static/css/styles.css`. When the class is applied, the button SHALL display a spinner animation (CSS-only) and reduced opacity to visually communicate that processing is in progress. The cursor SHALL change to `not-allowed`.

#### Scenario: Submit button loading state appearance
- **WHEN** a submit button has the `.is-submitting` class applied
- **THEN** it displays with reduced opacity, a spinner animation, and `cursor: not-allowed`

#### Scenario: Loading state uses CSS class not inline styles
- **WHEN** reviewing the submit button loading state implementation
- **THEN** all styling is applied via the `.is-submitting` class in `styles.css` with no inline `style` attributes
