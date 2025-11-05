# Testing Guide (pytest + behave + Playwright)

## Layers
- Unit (pytest): pure, fast, mock external boundaries.
- Integration (pytest): DB (SQLite/Postgres), filesystem, HTTP test servers.
- BDD (behave): user-facing behaviors; focus on business language.
- E2E (Playwright): critical paths only; keep fast and flaky-resistant.

## Pytest Conventions
- Tests live in `tests/`; name `test_*.py` / `*_test.py`.
- AAA pattern; one logical assertion group per test.
- Use fixtures in `tests/conftest.py` for session, client, temp dirs.
- Parametrize for edge cases; avoid loops in tests.

## DB Fixtures
- Local: ephemeral SQLite (file or in-memory) with migrations applied.
- CI/Prod-like: Postgres container (optional), URL via env.
- Provide a `session` fixture that rolls back between tests.

## Behave
- `.feature` files under `features/`.
- Steps in `features/steps/`, keep them reusable and declarative.
- Map steps to domain language, not UI specifics.

## Playwright
- Place tests in `e2e/`; use fixtures for auth, baseURL.
- Record trace/video on failure only; headless by default in CI.
- Seed data via API or DB fixture; clean up after.

## Commands
- Unit + integration: `pixi run test`
- BDD: `pixi run bdd`
- Playwright: `pixi run e2e`
