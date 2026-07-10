## 1. Templates Update

- [x] 1.1 Update the event creation template to use a `<form method="POST">` containing inputs for title, description, date, location, category_id, and a `{% csrf_token %}`.
- [x] 1.2 Add `required` HTML5 attributes to all required input fields in the creation form.
- [x] 1.3 Update the event list template to include a basic search/filter `<form method="GET">` for retrieving data.
- [x] 1.4 Create a new HTML template for User Registration with a `<form method="POST">` containing inputs for username and password.

## 2. Views Implementation

- [x] 2.1 Update the Event Create view to check `if request.method == "POST"`.
- [x] 2.2 In the POST handler, extract data from `request.POST`.
- [x] 2.3 Implement server-side validation to ensure required fields are present. If missing, return a 400 Bad Request or re-render the form indicating errors.
- [x] 2.4 If validation succeeds, create the Event record in the database.
- [x] 2.5 After successful creation, implement PRG by redirecting to the Event Detail or Event List view using `HttpResponseRedirect` or `redirect()`.
- [x] 2.6 Update GET handler on the event list view to accept and process query parameters (e.g., `request.GET.get('q')`) for basic searching or filtering.
- [x] 2.7 Implement User Registration view (e.g. in `users/views.py`) that handles GET (shows form) and POST (creates user and redirects).

## 3. Testing and Validation

- [x] 3.1 Manually verify form submissions via the browser (both successful creation and failing missing fields).
- [x] 3.2 Ensure CSRF token omission triggers a 403 Forbidden (verifying Django's CSRF middleware).
- [x] 3.3 Verify redirection happens successfully after a valid POST submission.
