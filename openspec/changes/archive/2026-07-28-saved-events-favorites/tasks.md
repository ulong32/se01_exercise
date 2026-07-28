## 1. Model & Migration

- [x] 1.1 Add `Favorite` model to `apps/events/models.py` with `user` FK, `event` FK, `created_at`, and `unique_together` constraint
- [x] 1.2 Run `python manage.py makemigrations events` to generate a new migration (do NOT edit existing migrations)
- [x] 1.3 Run `python manage.py migrate` to apply the migration

## 2. Admin Registration

- [x] 2.1 Register `Favorite` model in `apps/events/admin.py` with `list_display = ("user", "event", "created_at")`, `search_fields`, and `raw_id_fields`

## 3. Services & Selectors

- [x] 3.1 Add `toggle_favorite(user, event) -> bool` to `apps/events/services.py`
- [x] 3.2 Add `get_user_favorites(user) -> QuerySet[Event]` to `apps/events/selectors.py`
- [x] 3.3 Add `get_favorited_event_ids(user) -> set[int]` to `apps/events/selectors.py`

## 4. Views & URLs

- [x] 4.1 Add `event_toggle_favorite` view to `apps/events/views.py` (POST only, `@login_required`, returns `_favorite_button.html` partial)
- [x] 4.2 Add `event_saved` view to `apps/events/views.py` (GET, `@login_required`, renders saved events page)
- [x] 4.3 Update `event_list` view to pass `favorited_ids` set in template context
- [x] 4.4 Update `event_detail` view to pass `is_favorited` boolean in template context
- [x] 4.5 Add URL patterns in `apps/events/urls.py`: `saved/` (before `<int:event_id>/`) and `<int:event_id>/favorite/`

## 5. Templates

- [x] 5.1 Create `_favorite_button.html` partial with HTMX toggle (heart icon, `hx-post`, `hx-swap="outerHTML"`, CSRF header)
- [x] 5.2 Update `_event_results.html` to include `_favorite_button.html` in each event card (only for authenticated users)
- [x] 5.3 Update `event_detail.html` to include `_favorite_button.html` (only for authenticated users)
- [x] 5.4 Create `event_saved.html` template for the saved events listing page

## 6. Styling

- [x] 6.1 Add CSS for `.favorite-btn` and `.is-favorited` styles (heart icon, hover effects, transition)

## 7. Navigation

- [x] 7.1 Add "Saved Events" link to site navigation for authenticated users (in `base.html`)

## 8. Testing

- [x] 8.1 Test `toggle_favorite` service: first call creates favorite (returns True), second call deletes (returns False)
- [x] 8.2 Test `get_user_favorites` selector: returns correct events ordered by `created_at` desc
- [x] 8.3 Test `get_favorited_event_ids` selector: returns correct set, empty set for anonymous user
- [x] 8.4 Test toggle endpoint: authenticated POST toggles, unauthenticated redirects to login, GET returns 405
- [x] 8.5 Test saved events view: shows favorited events, empty state, unauthenticated redirects
- [x] 8.6 Test event list context includes `favorited_ids` for authenticated user
- [x] 8.7 Test event detail context includes `is_favorited` for authenticated user

## 9. Documentation

- [x] 9.1 Verify OpenSpec delta specs are complete and accurate against implementation
