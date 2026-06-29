# AGENTS.md

## Project scope

This is a Django web application for creating, browsing, searching, and managing local events.

Main apps:

- `apps/events` — event lifecycle, dynamic search, filtering, and pagination
- `apps/users` — user registration, authentication, and authorization (user vs. admin)
- `apps/api` — API endpoints for asynchronous UI updates (e.g., dynamic search)
- `apps/web` — server-rendered UI and rich frontend components

## Important project conventions

- Put business workflow logic in `services.py`, not in views or serializers.
- Put reusable read/query logic in `selectors.py`.
- Keep Celery tasks (if any) thin; they should call service functions.

## Commands

- Run server: `python manage.py runserver`
- Run tests: `pytest`
- Create migrations: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`
- Environment & deps: Use `uv` (e.g., `uv sync`)
- Linter/Formatter: `ruff check` / `ruff format`

## Things that are easy to break

- Event editing/deletion permissions (ensure only creators or admins can modify).
- Dynamic search and filtering logic (date, category, location).
- Pagination logic combined with filtering.

## Change coupling

If you change:

- a model → also check serializers, factories, and admin
- event models/fields → also check search filters, UI forms, and API responses
- permissions → also check both web views and API endpoints

## Constraints

- Do not edit old migrations; create a new one instead.
- Do not rename API fields or URL names unless explicitly asked.
- Prefer small, targeted changes over broad refactors.

## Documentation use

- Use `openspec/specs/*` as the canonical source for technical/runtime documentation.
- For project-level conventions, examine the `context` section of `openspec/config.yaml`.
- For system-specific tasks, read the relevant capability spec under `openspec/specs/<capability>/spec.md`.
- Use `openspec/notes/*` as supplemental context only for non-normative ideas and backlog notes.
- Keep technical/runtime truth in `openspec/specs/*`; promote accepted ideas from notes into specs.
- Keep documentation up to date. If inconsistency between code and documentation is detected, report it to the user and suggest a fix.
- When a new feature is implemented or a certain fact about the system is discovered, suggest reflecting it in documentation.

## Testing expectations

Add or update tests for:

- event search and date/category/location filtering
- permission changes (user vs. admin roles)
- UI submit protection logic (prevent duplicate entries)
