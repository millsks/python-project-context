# Tools & Commands

- Format: `pixi run fmt` (Ruff format + auto-fix)
- Format check: `pixi run fmt-check` (Ruff format check-only)
- Lint: `pixi run lint` (Ruff check)
- Type check: `pixi run mypy`
- Test (pytest): `pixi run test`
- BDD (behave): `pixi run bdd`
- E2E (Playwright): `pixi run e2e`
- All checks: `pixi run ci`

## Environment
- Default dev: Python >=3.11
- Local DB: SQLite (file in `.data/dev.db`)
- Prod DB: Postgres via `DATABASE_URL` env var
