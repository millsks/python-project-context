# Tools & Commands

- Format: `pixi run fmt` (Black + isort)
- Lint: `pixi run lint` (Ruff)
- Type check: `pixi run mypy`
- Test (pytest): `pixi run test`
- BDD (behave): `pixi run bdd`
- E2E (Playwright): `pixi run e2e`
- All checks: `pixi run ci`

## Environment
- Default dev: Python >=3.11
- Local DB: SQLite (file in `.data/dev.db`)
- Prod DB: Postgres via `DATABASE_URL` env var
