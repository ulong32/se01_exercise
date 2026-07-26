## ADDED Requirements

### Requirement: Skip Navigation Link
The system SHALL provide a "Skip to main content" link as the first focusable element in the base template. The link SHALL be visually hidden by default and become visible when it receives keyboard focus, allowing keyboard users to bypass repetitive navigation.

#### Scenario: Keyboard user skips navigation
- **WHEN** a keyboard user presses Tab on page load
- **THEN** a "Skip to main content" link becomes visible and, when activated, moves focus to the main content area

### Requirement: Semantic HTML Landmarks
The system SHALL use semantic HTML5 elements to define page structure: `<nav>` for navigation, `<main>` for primary content (with `id="main-content"`), `<header>` for the site header, and `<footer>` for the site footer. These elements SHALL serve as ARIA landmarks for assistive technology.

#### Scenario: Screen reader identifies page regions
- **WHEN** a screen reader user navigates the page by landmarks
- **THEN** the screen reader announces distinct regions for navigation, main content, header, and footer

### Requirement: ARIA Labels on Navigation
The system SHALL add `aria-label` attributes to `<nav>` elements to distinguish primary navigation from other navigational regions (e.g., `aria-label="Primary navigation"`).

#### Scenario: Multiple nav elements are distinguishable
- **WHEN** a page contains the site header navigation
- **THEN** the `<nav>` element has an `aria-label` attribute describing its purpose

### Requirement: Accessible Form Controls
The system SHALL associate every form input with a visible `<label>` element using matching `for`/`id` attributes. Form groups (label + input pairs) SHALL be wrapped in container elements for consistent spacing and layout.

#### Scenario: Label is associated with input
- **WHEN** a form is rendered (event create, login, register)
- **THEN** every `<input>`, `<textarea>`, and `<select>` element has a corresponding `<label>` with a `for` attribute matching the input's `id`

### Requirement: Accessible Error Messages
The system SHALL display error messages in containers with `role="alert"` so that screen readers announce errors immediately when they appear. Error text SHALL have sufficient color contrast against its background (minimum 4.5:1 ratio).

#### Scenario: Error message is announced by screen reader
- **WHEN** a form submission fails and an error message is displayed
- **THEN** the error container has `role="alert"` and the message is announced to screen reader users

### Requirement: Accessible Flash Messages
The system SHALL display Django messages framework notifications in a container with `role="status"` so that screen readers announce success and informational messages without interrupting the user's current task.

#### Scenario: Success message is announced
- **WHEN** an action completes successfully and a flash message is shown
- **THEN** the message container has `role="status"` and the message is announced politely by screen readers

### Requirement: Visible Focus Indicators
The system SHALL provide visible focus indicators on all interactive elements (links, buttons, form inputs) that meet WCAG 2.1 Level AA requirements. Focus outlines SHALL NOT be removed without providing an equivalent visible alternative.

#### Scenario: Keyboard focus is visible
- **WHEN** a user navigates the page using the Tab key
- **THEN** each focused element displays a clearly visible outline or border that contrasts with the surrounding content

### Requirement: Proper Heading Hierarchy
The system SHALL use a single `<h1>` element per page as the primary heading. Subsequent headings SHALL follow a logical hierarchy (`<h2>`, `<h3>`, etc.) without skipping levels.

#### Scenario: Page has correct heading structure
- **WHEN** any page is rendered
- **THEN** there is exactly one `<h1>` element and all subsequent headings follow a descending hierarchy without gaps
