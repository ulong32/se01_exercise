## Context

The project currently uses Django's default authentication system alongside custom domain models `Event` and `Category` defined in `apps/events/models.py`. However, `apps/events/admin.py` is unpopulated, meaning site administrators cannot manage these domain entities via the Django Admin interface. Additionally, establishing initial superuser credentials requires manual, interactive execution of `createsuperuser`, which hinders automated setup in development and test environments.

## Goals / Non-Goals

**Goals:**
- Register `Event` and `Category` models in `apps/events/admin.py` with comprehensive `ModelAdmin` options (list displays, filtering, and search).
- Implement a custom Django management command (`setup_admin`) that idempotently provisions or verifies an administrative superuser account using environment variables or safe defaults.

**Non-Goals:**
- Installing or configuring third-party admin styling themes (e.g., django-jazzmin, django-grappelli).
- Modifying the underlying database schema or permissions structure of existing domain models.

## Decisions

1. **Model Registration Design (`apps/events/admin.py`)**:
   - Use the `@admin.register` decorator for clean, declarative model registration.
   - For `EventModelAdmin`:
     - `list_display = ("title", "category", "date", "location", "creator")`
     - `list_filter = ("category", "date")`
     - `search_fields = ("title", "description", "location")`
     - `raw_id_fields = ("creator",)` to prevent loading thousands of user dropdown options if the database scales.
   - For `CategoryModelAdmin`:
     - `list_display = ("name",)`
     - `search_fields = ("name",)`

2. **Automated Admin Setup via Management Command**:
   - Implement `setup_admin.py` under `apps/users/management/commands/` (or `apps/events/management/commands/`).
   - Rationale: Unlike standard interactive commands, `setup_admin` can read `ADMIN_USERNAME`, `ADMIN_PASSWORD`, and `ADMIN_EMAIL` from environment variables, creating the superuser idempotently (`get_or_create` or checking existence before creation). This ensures frictionless developer onboarding and automated CI/CD readiness.

## Risks / Trade-offs

- [Risk] Hardcoded or predictable default credentials in local development could pose security risks if deployed to production without environment configuration. → Mitigation: Warn via console output when using fallback default credentials, and ensure production environments require explicit environment variables.
