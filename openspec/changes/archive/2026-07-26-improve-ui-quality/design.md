## Context

The Event Listings application currently has 7 Django templates (`base.html`, `home.html`, `event_list.html`, `event_detail.html`, `event_create.html`, `login.html`, `user_register.html`) with zero external CSS files. All visual styling is embedded as inline `style="..."` attributes — primarily `float`, `display:inline`, and `color:blue/red`. The application has a viewport meta tag but no CSS media queries or responsive layout rules. Semantic HTML is limited to basic `<header>`, `<main>`, and `<footer>` in `base.html`; child templates use generic `<div>` wrappers. There are no ARIA attributes, skip navigation links, or focus management patterns anywhere in the codebase.

Django's `django.contrib.staticfiles` app is already in `INSTALLED_APPS`, and `STATIC_URL` is set to `'static/'`, but no `STATICFILES_DIRS` is configured and no static files exist.

## Goals / Non-Goals

**Goals:**
- Separate all presentation from structure by extracting inline styles into an external CSS file
- Establish a responsive layout that works across mobile (≤ 576px), tablet (577–768px), and desktop (769px+) viewports
- Improve semantic HTML structure in all templates
- Add baseline accessibility features (skip nav, ARIA landmarks, focus indicators, form labels, error roles)
- Configure Django static file serving for the new CSS

**Non-Goals:**
- JavaScript-powered interactivity or dynamic UI components
- CSS preprocessors (Sass, Less) or CSS frameworks (Bootstrap, Tailwind)
- Theming system or design tokens — a single CSS file is sufficient at this scale
- Rewriting view logic, models, or URL routing
- Production-grade static file deployment (collectstatic, CDN)

## Decisions

### Decision 1: Single global CSS file vs. per-app CSS files

**Choice**: Single `static/css/styles.css` at the project root.

**Rationale**: The project has only 7 templates sharing a common layout. Per-app splitting would add complexity (multiple `{% static %}` tags, load order concerns) with no benefit at this scale. If the project grows, the file can be split later.

**Alternative considered**: Per-app static directories (`apps/events/static/events/css/`). Rejected because it fragments a cohesive design system and complicates cascade ordering.

### Decision 2: Layout technique — Flexbox vs. CSS Grid vs. Float

**Choice**: CSS Flexbox for header navigation and page layout; CSS Grid is not needed.

**Rationale**: The current layout uses `float: left/right` for the header, which causes clearfix issues and doesn't adapt to screen sizes. Flexbox handles 1-dimensional navigation layouts cleanly with `justify-content: space-between` and wraps naturally on narrow screens. Grid would be overkill for these layouts.

### Decision 3: Responsive breakpoints

**Choice**: Mobile-first approach with two breakpoints:
- `min-width: 577px` — tablet: side-by-side header layout
- `min-width: 769px` — desktop: wider content area, larger spacing

**Rationale**: Mobile-first ensures the smallest screens get a functional layout by default, and media queries progressively enhance. Two breakpoints cover the practical device spectrum without over-engineering.

### Decision 4: Static files directory configuration

**Choice**: Add `STATICFILES_DIRS = [BASE_DIR / 'static']` to `config/settings.py`, and create `static/css/styles.css`.

**Rationale**: This uses Django's standard convention for project-level static files. The `staticfiles` app is already installed and `STATIC_URL` is already set. Only `STATICFILES_DIRS` is missing.

### Decision 5: Accessibility scope

**Choice**: Target WCAG 2.1 Level A compliance with selected Level AA features (color contrast, focus indicators).

**Rationale**: Level A is the minimum legal standard in many jurisdictions and covers the most critical barriers (text alternatives, keyboard navigation, semantic structure). Adding focus indicators and contrast from Level AA is low-effort and high-impact.

## Risks / Trade-offs

- **Risk**: Removing inline styles may temporarily break visual appearance during incremental implementation → **Mitigation**: All inline style removal and CSS class addition happen in the same task, tested together.
- **Risk**: New CSS classes could conflict with future CSS framework adoption → **Mitigation**: Use descriptive, component-scoped class names (e.g., `.site-header`, `.event-card`) that are easy to map or remove.
- **Trade-off**: Mobile-first CSS means desktop styles are behind media queries, slightly more verbose → Acceptable trade-off for better mobile support by default.
- **Trade-off**: Single CSS file means all pages load all styles → At current file size (~200 lines), this has negligible performance impact.
