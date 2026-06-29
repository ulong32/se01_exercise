# AGENTS.md

## Project scope

This is a Django app for managing customer orders and internal staff workflows.

Main apps:

- `apps/orders` — order lifecycle
- `apps/accounts` — users and roles
- `apps/api` — DRF endpoints
- `apps/web` — staff-facing server-rendered UI

## Important project conventions

- Put business workflow logic in `services.py`, not in views or serializers.
- Put reusable read/query logic in `selectors.py`.
- Keep Celery tasks thin; they should call service functions.

## Commands

- Run server: `python manage.py runserver`
- Run tests: `pytest`
- Create migrations: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`

## Things that are easy to break

- API response shapes in `apps/api`
- role/permission checks in `apps/accounts`
- order status transitions in `apps/orders/services.py`

## Change coupling

If you change:

- a model → also check serializers, factories, and admin
- order workflow → also check tasks and notifications
- permissions → also check both web views and API endpoints

## Constraints

- Do not edit old migrations; create a new one instead.
- Do not rename API fields or URL names unless explicitly asked.
- Prefer small, targeted changes over broad refactors.

## Documentation use

- Use `openspec/specs/*` as the canonical source for technical/runtime documentation.
- For project-level conventions, examine the `context` section of `openspec/config.yaml`.
- For system-specific tasks, read the relevant capability spec under `openspec/specs/<capability>/spec.md` (for example: `user-management`, `purchase-order`).
- Use `openspec/notes/*` as supplemental context only for non-normative ideas and backlog notes.
- Keep technical/runtime truth in `openspec/specs/*`; promote accepted ideas from notes into specs.
- Keep documentation up to date. If inconsistency between code and documentation is detected, report it to the user and suggest a fix.
- When a new feature is implemented or a certain fact about the system is discovered, suggest reflecting it in documentation.

## Testing expectations

Add or update tests for:

- order status changes
- permission changes
- API response changes
