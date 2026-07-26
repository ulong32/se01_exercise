## 1. Static Files Infrastructure

- [x] 1.1 Add `STATICFILES_DIRS = [BASE_DIR / 'static']` to `config/settings.py`
- [x] 1.2 Create directory `static/css/` and an empty `styles.css` file
- [x] 1.3 Update `templates/base.html` to load `{% load static %}` and link `<link rel="stylesheet" href="{% static 'css/styles.css' %}">`
- [x] 1.4 Verify the CSS file is served by running the dev server and requesting the CSS URL

## 2. Base Template Restructuring

- [x] 2.1 Add skip navigation link (`<a href="#main-content" class="skip-link">Skip to main content</a>`) as the first element in `<body>`
- [x] 2.2 Replace header's `<div style="float:...">` layout with `<nav aria-label="Primary navigation">` using CSS Flexbox classes
- [x] 2.3 Remove all inline `style="..."` attributes from `base.html` and replace with CSS classes (`.site-header`, `.site-nav`, `.nav-links`, `.messages-list`, `.site-footer`)
- [x] 2.4 Add `id="main-content"` to the `<main>` element for skip navigation target
- [x] 2.5 Add `role="status"` to the messages container for screen reader announcements


## 3. CSS Stylesheet — Base Styles

- [x] 3.1 Write CSS reset/normalize rules (box-sizing, margin/padding resets)
- [x] 3.2 Write typography rules (font-family, base font-size, line-height, heading sizes)
- [x] 3.3 Write skip-link styles (visually hidden by default, visible on `:focus`)
- [x] 3.4 Write site header/nav styles using Flexbox (`justify-content: space-between`, `align-items: center`, `flex-wrap: wrap`)
- [x] 3.5 Write main content container styles (max-width, centered, horizontal padding)
- [x] 3.6 Write footer styles
- [x] 3.7 Write focus indicator styles for interactive elements (`:focus-visible` outline)

## 4. CSS Stylesheet — Responsive Design

- [x] 4.1 Write mobile-first base styles (stacked nav, full-width forms, full-width content)
- [x] 4.2 Write `@media (min-width: 577px)` tablet breakpoint (side-by-side nav, constrained form widths)
- [x] 4.3 Write `@media (min-width: 769px)` desktop breakpoint (wider max-width, larger spacing)

## 5. CSS Stylesheet — Component Styles

- [x] 5.1 Write form styles (`.form-group` with label/input spacing, full-width inputs on mobile, constrained on desktop)
- [x] 5.2 Write button styles (`.btn`, `.btn-primary` with consistent padding, color, hover/focus states)
- [x] 5.3 Write event list item styles (`.event-list`, `.event-item` as card-like layout)
- [x] 5.4 Write event detail styles (`.event-detail`, definition list or structured layout for attributes)
- [x] 5.5 Write error/alert message styles (`.alert`, `.alert-error`, `.alert-info` with sufficient contrast and `role` attributes)
- [x] 5.6 Write search form styles (`.search-form` inline layout on desktop, stacked on mobile)

## 6. Event Templates Restructuring

- [x] 6.1 Update `events/home.html` — use semantic HTML, CSS classes, remove inline styles, ensure single `<h1>`
- [x] 6.2 Update `events/event_list.html` — replace `<ul>/<li>` with semantic event items (`.event-list` / `.event-item`), add `<label>` to search input, use CSS classes
- [x] 6.3 Update `events/event_detail.html` — use structured markup (`.event-detail`) for event attributes with `<dl>`/`<dt>`/`<dd>` or sectioned layout, remove inline styles
- [x] 6.4 Update `events/event_create.html` — wrap each label/input pair in `.form-group` divs, remove `<br>` tags, ensure `for`/`id` associations, use CSS classes

## 7. User Templates Restructuring

- [x] 7.1 Update `users/login.html` — wrap label/input pairs in `.form-group` divs, remove `<br>` tags, add `role="alert"` to error message container, replace inline `style="color: red;"` with CSS class
- [x] 7.2 Update `users/user_register.html` — wrap label/input pairs in `.form-group` divs, remove `<br>` tags, add `role="alert"` to error message container, replace inline `style="color: red;"` with CSS class

## 8. Verification

- [x] 8.1 Run the dev server and visually verify all pages render correctly with the external stylesheet
- [x] 8.2 Verify no inline `style="..."` attributes remain in any template (grep check)
- [x] 8.3 Test responsive layout at 375px (mobile), 768px (tablet), and 1024px (desktop) viewport widths
- [x] 8.4 Test keyboard navigation: verify skip link works, all interactive elements are focusable with visible indicators, and Tab order is logical
- [x] 8.5 Run existing tests (`pytest`) to confirm no regressions in view behavior

