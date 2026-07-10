## 1. View Functions

- [x] 1.1 Implement `home` view in `apps/events/views.py` — returns an HttpResponse with a welcome message for GET `/`
- [x] 1.2 Implement `event_list` view — queries all Event objects and returns a summary (title, date, location) as an HttpResponse
- [x] 1.3 Implement `event_detail` view — accepts `event_id`, returns full event details or 404 if not found
- [x] 1.4 Implement `event_create` view (GET) — returns an HttpResponse with a placeholder form description
- [x] 1.5 Implement `event_create` view (POST) — processes POST data to create a new Event with hard-coded creator, redirects to detail page on success, returns 400 on missing fields

## 2. URL Routing

- [x] 2.1 Create `apps/events/urls.py` with URL patterns for all five view endpoints, using `app_name = "events"` namespace
- [x] 2.2 Update `config/urls.py` to include events app URLs using `include()` — home page at `/`, events at `/events/`

## 3. Testing

- [x] 3.1 Add view tests in `tests/test_views.py` — test home page returns 200, event list returns 200, event detail returns 200 for existing and 404 for non-existent, create returns 200 on GET and creates event on POST
- [x] 3.2 Run the full test suite (`pytest`) and verify all tests pass

## 4. Documentation

- [x] 4.1 Update `README.md` with a URL API section documenting all callable URLs, their HTTP methods, arguments, and return values
- [x] 4.2 Update OpenSpec specs to reflect the new views capability (sync delta specs if needed)
