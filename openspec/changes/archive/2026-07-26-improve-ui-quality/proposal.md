## Why

The current UI has no external CSS files — all styling is inline (`style="..."` attributes) directly in Django templates. This violates the separation of structure and presentation, makes maintenance difficult, and produces an unstyled, inaccessible interface. The templates also lack semantic HTML elements (`<nav>`, `<section>`, `<article>`), ARIA attributes, skip navigation, and responsive layout techniques. As the project grows, these foundational gaps will compound, so addressing them now is the right time.

## What Changes

- **Extract all inline styles to external CSS files**: Create a project-wide `static/css/styles.css` loaded via Django's `{% static %}` tag in `base.html`. Remove every `style="..."` attribute from templates.
- **Add responsive layout with CSS**: Use CSS Flexbox/Grid and media queries to ensure the interface works correctly on mobile, tablet, and desktop viewports. Introduce a responsive navigation header that adapts to small screens.
- **Improve semantic HTML structure**: Replace generic `<div>` wrappers with semantic elements (`<nav>`, `<section>`, `<article>`, `<aside>`) across all templates. Use proper heading hierarchy (`<h1>` once per page, followed by `<h2>`, `<h3>` as needed).
- **Add accessibility features**: Include skip-navigation links, ARIA landmarks and labels, `role="alert"` on error/message containers, visible focus indicators, sufficient color contrast, and proper `<label>` association with form controls.
- **Configure Django static files**: Add `STATICFILES_DIRS` to `config/settings.py` so the new CSS file is discoverable by `django.contrib.staticfiles`.

## Capabilities

### New Capabilities
- `ui-styling`: Defines requirements for CSS-based styling, responsive design, and the separation of structure from presentation across all templates.
- `accessibility`: Defines requirements for WCAG-aligned accessibility features including semantic HTML, ARIA attributes, keyboard navigation, and color contrast.

### Modified Capabilities
- `basic-views`: Views must now render templates that use external CSS, semantic HTML, and accessibility attributes. No behavioral changes to view logic.

## Impact

- **Templates**: All 7 templates (`base.html`, `home.html`, `event_list.html`, `event_detail.html`, `event_create.html`, `login.html`, `user_register.html`) will be restructured with semantic HTML and external CSS classes.
- **Static files**: New `static/css/styles.css` file; `config/settings.py` gains `STATICFILES_DIRS`.
- **No backend logic changes**: Views, models, URLs, and services remain unchanged.
- **No database changes**: No migrations needed.
- **No API changes**: No URL names or API fields are renamed.
