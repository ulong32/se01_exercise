## Context

The application manages local events with Django (events CRUD, user auth, HTMX-driven search/filter). Currently there is no relationship between users and events beyond the `creator` foreign key. Users cannot bookmark events. The proposal calls for a "Saved Events" feature with an explicit junction model, HTMX-driven toggle UI, and a dedicated saved events page.

Existing architecture:
- Business logic in `services.py`, read logic in `selectors.py` (per AGENTS.md)
- HTMX partial rendering pattern: views detect `HX-Request` header and return partials
- Templates use `_` prefix for HTMX partials (e.g., `_event_results.html`)

## Goals / Non-Goals

**Goals:**
- Enable authenticated users to favorite/unfavorite events with a single click
- Provide a dedicated "Saved Events" page listing a user's bookmarked events
- Seamless HTMX toggle without full-page reload
- Follow the existing services/selectors architecture pattern
- Maintain progressive enhancement (works without JS)

**Non-Goals:**
- Social features (sharing favorites, seeing other users' favorites)
- Notification system for favorited events (e.g., reminders)
- Sorting/filtering within the saved events page (can be added later)
- API (DRF) endpoints for favorites — only Django views for now

## Decisions

### 1. Explicit `Favorite` junction model vs. `ManyToManyField`

**Decision**: Use an explicit `Favorite(user, event, created_at)` model.

**Alternatives considered**:
- `Event.favorited_by = ManyToManyField(User)`: Simpler, but no `created_at` timestamp, no easy admin customization, and harder to extend later (e.g., adding notes).

**Rationale**: The explicit model gives us a `created_at` timestamp for ordering "recently saved" events, enables a dedicated admin view, and allows future extensibility (e.g., adding categories/notes to bookmarks). The overhead is minimal — one extra model and migration.

### 2. Toggle endpoint returns HTMX partial

**Decision**: `POST /events/<id>/favorite/` toggles the state and returns a `_favorite_button.html` partial reflecting the new state. The partial swaps the button in-place via `hx-swap="outerHTML"`.

**Alternatives considered**:
- Return JSON + client-side JS manipulation: Adds JS complexity, breaks the server-rendered HTMX pattern used throughout.
- Redirect-based approach: Would cause full-page reload, poor UX.

**Rationale**: Consistent with the existing HTMX partial pattern used for search/pagination. The server renders the button HTML with the correct state and the client just swaps it in.

### 3. CSRF handling for HTMX POST

**Decision**: Use `hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'` on the favorite button form/element.

**Rationale**: Standard Django CSRF protection. The HTMX docs recommend this approach. The `csrf_token` is already available in all templates via Django's context processors.

### 4. Favorite button placement

**Decision**: Add the favorite button to both event cards (`_event_results.html`) and the event detail page (`event_detail.html`). For cards, use a small heart icon in the corner. For detail, use a larger "Save / Saved" button.

**Rationale**: Users should be able to favorite from wherever they see events. The card icon is compact to avoid clutter; the detail button can be more prominent.

### 5. Saved events page at `/events/saved/`

**Decision**: Place the saved events URL before `<int:event_id>/` in the URL patterns to avoid "saved" being interpreted as an event ID.

**Rationale**: Django's URL resolver matches top-to-bottom; `<int:event_id>` would not match "saved" (it's not an int), but explicit ordering is clearer and safer.

### 6. Unauthenticated users see no favorite button

**Decision**: The favorite button is only rendered for authenticated users (`{% if user.is_authenticated %}`). Anonymous users see no button.

**Alternatives considered**:
- Show a disabled button linking to login: Adds complexity for minimal gain at this stage.

**Rationale**: Simple and clean. Avoids confusing anonymous users with a button that would redirect them to login.

## Risks / Trade-offs

- **N+1 queries on event list**: Checking `is_favorited` per event card could cause N+1 queries. → **Mitigation**: Prefetch the user's favorited event IDs in the view and pass the set to the template context, using `{% if event.id in favorited_ids %}` instead of per-event DB lookups.
- **URL collision with `/events/saved/`**: If a future event ID scheme changes (unlikely with `<int:event_id>`) → **Mitigation**: URL order and type constraint already prevent this.
- **Template complexity**: Adding favorite button logic to existing card partial → **Mitigation**: Extract the button into its own `_favorite_button.html` partial and use `{% include %}` in both the card and detail templates.
