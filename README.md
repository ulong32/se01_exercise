# Event Listings Web Application

A web application that allows users to create, browse, search, and manage local events. It features dynamic searching and filtering to provide a seamless user experience.

## Core Features

* Authentication: User registration and login functionality.
* Event Management: Event creation, editing, and deletion (restricted to the original creator or system administrators).
* Search & Filtering: Substring search for titles, plus filtering by date, category, and location.
* Browsing & Pagination: Paginated event lists with past events hidden or visually grayed out.
* Rich UI: Asynchronous dynamic search updates without page reloads, visual calendar widgets, and submit protection to prevent duplicate entries.


## Development Environment

* Language: Python 3.12.3
* Package & Environment Manager: uv
* Linter & Formatter: Ruff
* Testing & Coverage: pytest, pytest-cov
* Database: Relational Database (SQL)

## Setup Instructions

1. Create and activate the virtual environment:
```bash
   uv venv --python 3.12
   # For Mac/Linux:
   source .venv/bin/activate
   # For Windows:
   .venv\Scripts\activate

```

2. Install dependencies:
```bash
uv sync

```

## URL API

The application currently exposes the following simple view endpoints:

| URL Pattern | Method | Description | Return Format |
|---|---|---|---|
| `/` | GET | Welcome page | Plain text (`HttpResponse`) |
| `/events/` | GET | List all events | JSON (`JsonResponse`) (plain text `HttpResponse` message when no events exist) |
| `/events/<id>/` | GET | Event details | JSON (`JsonResponse`) |
| `/events/create/` | GET | Show create form (stub) | Plain text (`HttpResponse`) |
| `/events/create/` | POST | Create an event | Redirect to `/events/<id>/` |
| `/events/<id>/edit/` | GET | Show edit form | HTML (`HttpResponse`) |
| `/events/<id>/edit/` | POST | Update an event | Redirect to `/events/<id>/` |
| `/events/<id>/delete/` | POST | Delete an event | Redirect to `/events/` |

*Note: The create and edit POST endpoints expect `title`, `description`, `date`, `location`, and `category_id` in the form data.*

## Database Schema

The application relies on the following primary tables:

* `users`: User account information and authorization roles (user vs. admin).
* `events`: Detailed event information (title, date, location, category) linked to the creator's ID.
* *(Optional)* `favorites`: A junction table mapping the many-to-many relationship for users' saved events.
