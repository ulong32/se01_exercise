# Event Listings Web Application

A Django-based web application that allows users to create, browse, search, and manage local events. It features dynamic searching and filtering to provide a seamless user experience.

## Core Features

* Authentication: User registration and login functionality.
* Event Management: Event creation, editing, and deletion (restricted to the original creator or system administrators).
* Search & Filtering: Substring search for titles, plus filtering by date, category, and location.
* Browsing & Pagination: Paginated event lists with past events hidden or visually grayed out.
* Favorites: Users can save/favorite events they are interested in.
* Rich UI: Asynchronous dynamic search updates without page reloads, visual calendar widgets, and submit protection to prevent duplicate entries.

## Project Structure

* `apps/events/`: Contains the core event lifecycle logic, models, services, selectors, views, and urls.
* `apps/users/`: Manages user registration, authentication, and sessions.
* `config/`: The main Django project configuration, settings, and root URLs.
* `docs/`: Detailed specification documents for each file in the project.

## Development Environment

* Language: Python 3.12
* Package & Environment Manager: uv
* Framework: Django
* Linter & Formatter: Ruff
* Testing & Coverage: pytest, pytest-cov
* Database: Relational Database (SQL - SQLite by default)

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

3. Run migrations:
```bash
python manage.py migrate
```

4. Run the development server:
```bash
python manage.py runserver
```

## URL APIs

### Events App (`/events/`)

| URL Pattern | Method | Description |
|---|---|---|
| `/events/` | GET | List all events |
| `/events/saved/` | GET | List events favorited by the current user |
| `/events/<id>/` | GET | Event details |
| `/events/<id>/favorite/` | POST | Toggle favorite status for an event |
| `/events/create/` | GET/POST | Create a new event |
| `/events/<id>/edit/` | GET/POST | Update an existing event |
| `/events/<id>/delete/` | POST | Delete an event |

### Users App (`/users/`)

| URL Pattern | Method | Description |
|---|---|---|
| `/users/register/` | GET/POST | User registration |
| `/users/login/` | GET/POST | User login |
| `/users/logout/` | GET/POST | User logout |

## Database Schema

The application relies on the following primary tables:

* `users`: User account information and authorization roles (user vs. admin).
* `events_category`: Event categories.
* `events_event`: Detailed event information (title, date, location, category) linked to the creator's ID.
* `events_favorite`: A junction table mapping the many-to-many relationship for users' saved events.
