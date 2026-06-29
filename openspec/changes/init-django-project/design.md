## Context

We are creating a new Django project for event management. The project is at the very beginning of its lifecycle. We need to set up the default Django directory structure, configure settings, and establish the initial database schema (Models) with `__str__` representations to support the admin panel.
Additionally, the user requested professional development workflows including the use of OpenSpec, GitHub issues, branch management, unit tests, and code reviews.

## Goals / Non-Goals

**Goals:**
- Initialize the Django project structure using `django-admin startproject` and `manage.py startapp`.
- Define `User`, `Event`, and `Category` models in the new app's `models.py`.
- Configure the default SQLite database (for simplicity of initial setup).
- Create automated unit tests for the models and their `__str__` methods.
- Define a structured workflow utilizing GitHub issues, feature branches, and code review practices.

**Non-Goals:**
- Setting up a production database like PostgreSQL at this stage.
- Implementing the web views, templates, or REST APIs (these will come in subsequent tasks).
- Detailed styling or frontend work.

## Decisions

- **Application Structure:** 
  - We will name the Django project `config` or similar standard wrapper, and the main app `events` (as per the `AGENTS.md` project scope).
- **Database Schema (Models):**
  - `Category`: `name` (CharField)
  - `User`: Extend Django's AbstractUser or just use the default User model for now (we'll assume default or simple extension depending on needs, likely default `django.contrib.auth.models.User` to keep it simple, or as requested).
  - `Event`: `title` (CharField), `description` (TextField), `date` (DateTimeField), `location` (CharField), `category` (ForeignKey to Category), `creator` (ForeignKey to User).
- **Unit Testing Framework:**
  - We will use `pytest` and `pytest-django` as recommended by the `AGENTS.md` rules.

## Risks / Trade-offs

- **Risk:** Initial schema might miss fields needed later.
  - **Mitigation:** Django migrations make it easy to modify schemas later. Start minimal.
- **Risk:** Complex testing setup.
  - **Mitigation:** Keep the tests focused on the models and string representations for now.
