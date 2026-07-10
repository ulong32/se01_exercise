# Web Application Design: State Handling and Page Structure

## 1. State Handling

### What information should be remembered between requests?
* **Authentication State:** Whether the user is currently logged in, and if so, their user ID and roles (e.g., normal user vs. admin).
* **Search and Filter Parameters:** When a user is browsing events, their current search queries, selected categories, location filters, and pagination state. This is often best done via URL query parameters (e.g., `?category=music&page=2`) rather than server-side state, to allow bookmarking and sharing.
* **User Feedback (Flash Messages):** Temporary messages to display on the next page load, such as "Event successfully created" or "Invalid login credentials."

### What should be stored in the database?
Persistent data that forms the core of the application should live in the database:
* **Users:** User accounts, hashed passwords, email addresses, and profile information (`apps/users`).
* **Events:** Event details including title, description, date, time, location, category, and the ID of the user who created it (`apps/events`).
* **Relationships/Interactions:** Records of which users are attending which events, comments, or event ratings.
* **System Data:** Predefined categories, tags, or locations.

### What should be stored in a session?
Data that is temporary, specific to a single user's current browsing period, and sensitive or not suitable for URLs:
* **Session ID / Auth Tokens:** To identify the logged-in user across requests securely.
* **CSRF Tokens:** For protecting forms against Cross-Site Request Forgery attacks.
* **Flash Messages:** Using Django's messages framework, these are temporarily stored in the session until displayed.
* **Incomplete Form Data (Optional):** If a user is filling out a multi-step form (e.g., a complex event creation wizard), temporary progress could be stored in the session.

---

## 2. Template-Based Page Structure

### What common page structure will be reused?
The application should use a base template (e.g., `base.html`) that defines the overarching HTML skeleton. Common elements include:
* **`<head>` Section:** Meta tags, title block, links to CSS stylesheets, and base JavaScript files.
* **Header / Navigation Bar:** 
    * Branding/Logo.
    * Main navigation links (Home, Browse Events).
    * Context-aware user actions (Login/Register if guest; Profile, Create Event, Logout if logged in).
* **Footer:** Copyright information, links to terms of service, privacy policy, and contact info.
* **Message Container:** A dedicated block to render any flash messages (success, error, warning) from the session.
* **Main Content Block:** A placeholder (`{% block content %}{% endblock %}`) where individual pages will inject their specific content.

### Which pages should share the same layout?
* **Standard Layout (`base.html`):** Most user-facing pages will inherit from the standard base layout. This includes:
    * Home/Landing Page
    * Event Listing/Search Results Page
    * Event Detail Page
    * Event Creation/Edit Forms
    * User Profile Page
* **Authentication Layout (Optional):** Login, registration, and password reset pages might share a slightly modified, cleaner layout (e.g., `auth_base.html`) without the full navigation bar to minimize distractions.
* **Admin Layout:** Django provides its own layout for the administrative interface, which operates independently of the public-facing templates.
