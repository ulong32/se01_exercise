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
