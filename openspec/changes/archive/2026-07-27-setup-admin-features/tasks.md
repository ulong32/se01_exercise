## 1. Django Admin Model Registration

- [x] 1.1 In `apps/events/admin.py`, register `Category` with `CategoryModelAdmin` configuring `list_display` and `search_fields`
- [x] 1.2 In `apps/events/admin.py`, register `Event` with `EventModelAdmin` configuring `list_display`, `list_filter`, `search_fields`, and `raw_id_fields`

## 2. Admin User Setup Management Command

- [x] 2.1 Create directory structure `apps/users/management/commands/` with necessary `__init__.py` files
- [x] 2.2 Implement `setup_admin.py` management command in `apps/users/management/commands/` to idempotently create or verify an administrative superuser account

## 3. Verification & Testing

- [x] 3.1 Write tests verifying that `setup_admin` creates a superuser when none exists and runs without error when one already exists
- [x] 3.2 Execute test suite (`pytest`) to verify all tests pass and admin registration causes no regressions
