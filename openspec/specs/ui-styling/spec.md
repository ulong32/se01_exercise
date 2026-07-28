# ui-styling Specification

## Requirements

### Requirement: External CSS Stylesheet
The system SHALL load all presentation styles from an external CSS file (`static/css/styles.css`) linked in the base template via Django's `{% static %}` tag. No inline `style="..."` attributes SHALL remain in any template.

#### Scenario: Base template links external CSS
- **WHEN** any page is rendered
- **THEN** the HTML `<head>` contains a `<link>` element referencing the external stylesheet via `{% static 'css/styles.css' %}`

#### Scenario: No inline styles in templates
- **WHEN** reviewing any Django template in the project
- **THEN** no `style="..."` attributes are present in the HTML markup

### Requirement: Django Static Files Configuration
The system SHALL configure `STATICFILES_DIRS` in `config/settings.py` to include the project-level `static/` directory so that `django.contrib.staticfiles` can discover and serve the CSS file.

#### Scenario: Static file is served in development
- **WHEN** the development server is running and a browser requests the CSS file URL
- **THEN** the server returns the CSS file with HTTP 200

### Requirement: Responsive Navigation Header
The system SHALL render the site header navigation using CSS Flexbox layout that adapts to different screen sizes. On mobile viewports (≤ 576px), navigation items SHALL stack vertically. On tablet and desktop viewports (≥ 577px), navigation items SHALL display in a horizontal row with the site title on the left and user actions on the right.

#### Scenario: Header on mobile viewport
- **WHEN** the page is viewed on a viewport width of 576px or less
- **THEN** the header displays the site title and navigation links stacked vertically with centered alignment

#### Scenario: Header on desktop viewport
- **WHEN** the page is viewed on a viewport width of 769px or more
- **THEN** the header displays the site title on the left and user action links on the right in a single horizontal row

### Requirement: Responsive Content Layout
The system SHALL apply a maximum content width and centered layout on desktop viewports, while allowing full-width content on mobile viewports. Form elements SHALL expand to full width on mobile and constrain to a readable width on larger screens.

#### Scenario: Content area on desktop
- **WHEN** the page is viewed on a desktop viewport
- **THEN** the main content area is centered with a maximum width and horizontal padding

#### Scenario: Form layout on mobile
- **WHEN** a form page (event create, login, register) is viewed on a mobile viewport
- **THEN** all form inputs and buttons expand to full width for easy tap targets

### Requirement: Consistent Visual Styling via CSS Classes
The system SHALL use CSS classes (not inline styles) for all visual presentation including typography, spacing, colors, and layout. Templates SHALL apply descriptive class names (e.g., `.site-header`, `.event-list`, `.form-group`) that map to rules in the external stylesheet.

#### Scenario: Template uses CSS classes for styling
- **WHEN** a template element requires visual styling
- **THEN** it uses a CSS class defined in `styles.css` rather than an inline `style` attribute

### Requirement: Responsive Event List
The system SHALL display the event list in a structured format that is readable on all screen sizes. Each event item SHALL show the event title as a link, along with the date and location.

#### Scenario: Event list on mobile
- **WHEN** the event list page is viewed on a mobile viewport
- **THEN** each event is displayed as a stacked card with the title, date, and location on separate lines

#### Scenario: Event list on desktop
- **WHEN** the event list page is viewed on a desktop viewport
- **THEN** each event is displayed with the title, date, and location visible in a structured layout

### Requirement: Past Event Visual Distinction
The system SHALL style past events with a distinct grayed-out visual appearance using the CSS class `past-event`. The CSS rule SHALL apply `opacity: 0.6` and `filter: grayscale(60%)`. Hover effects on past event cards SHALL be muted compared to upcoming events (no upward lift animation, standard shadow).

#### Scenario: Past event styling rules
- **WHEN** an element has the class `past-event` applied
- **THEN** it renders with 60% opacity and 60% grayscale filter

#### Scenario: Past event hover styling
- **WHEN** a user hovers over a `.past-event` card
- **THEN** the card does NOT lift upwards (`transform: none`) and maintains a subdued border and shadow

### Requirement: Pagination Navigation Styling
The system SHALL style the pagination navigation controls using the `.pagination` and `.pagination-link` classes in `static/css/styles.css`. The container SHALL use a centered Flexbox layout with wrapping and gap spacing. Individual page links SHALL be pill-shaped with consistent padding and transitions. The active page link (`.pagination-link.active`) SHALL use the brand accent gradient background with bold white text. Disabled links (`.pagination-link.disabled`) SHALL have reduced opacity (`0.4`) and a not-allowed cursor.

#### Scenario: Pagination container layout
- **WHEN** the `.pagination` container is rendered
- **THEN** it displays its children centered horizontally with a gap between elements and wrapping on small screens

#### Scenario: Active page number styling
- **WHEN** the current page number is rendered with class `.pagination-link.active`
- **THEN** it displays with the accent gradient background, no border, and bold white text

#### Scenario: Disabled pagination link styling
- **WHEN** a Previous or Next link is disabled at the boundaries of the page range
- **THEN** it renders with 0.4 opacity and `cursor: not-allowed` without hover color changes

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
