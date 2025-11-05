# Copilot Context (Python + Conda/Pixi + Testing)

## Coding Style (Global)
- Follow PEP 8 with spaces over tabs; line length 100.
- Prefer readability and explicitness; avoid clever one-liners.
- Small, single-purpose functions; return early when clear.
- Type hints everywhere; enable strict-ish checks.
- Docstrings for public APIs (Google style preferred).

## Project Structure
- `src/<package_name>/` for library/app code.
- `tests/` for unit/integration (pytest).
- `features/` for BDD (behave).
- `e2e/` for Playwright tests.
- `scripts/` for CLI scripts (idempotent).
- `examples/` for runnable patterns/templates.

## Error Handling
- Use custom exceptions per module/package for domain errors.
- Never swallow exceptions silently; log context with structured fields.

## I/O & DB
- Local dev: SQLite with `sqlite3` or SQLAlchemy + SQLite URL.
- Prod: Postgres (SQLAlchemy URL via env var, e.g., `DATABASE_URL`).
- Abstract DB behind a repository interface; inject the engine/session.

## Testing
- Unit tests: fast, deterministic, Arrange-Act-Assert.
- BDD specs in `features/` with clear Given/When/Then.
- E2E in Playwright; prefer data seeding via API/fixtures.
- Use pytest fixtures; avoid global mutable state.

## Security
- No secrets in repo. Load via env vars or secret manager.
- Validate and sanitize inputs at boundaries.
- Use parameterized queries/ORM; never string-concatenate SQL.

## Tooling Defaults
- Env/tasks: Pixi (`pixi.toml`).
- Format: Ruff (line-length 100, includes import sorting).
- Lint: Ruff (E,F,I,B,UP,ANN,SIM).
- Type check: MyPy (strict-ish).
- Tests: pytest; behave; Playwright (headed in CI only if needed).

## Code Patterns We Prefer
- Dependency injection for services (DB, HTTP clients, time).
- Pure domain functions; thin adapters for I/O.
- Configuration via env vars with typed config loader.

## Anti-Patterns (Avoid)
- Large functions (>80 lines) or deep nesting (>2 levels).
- Implicit global state; side effects in import time.
- Mixing sync/async unless necessary and well-isolated.

## Example: Repository pattern (SQLAlchemy)
```py
from typing import Protocol, Optional
from sqlalchemy.orm import Session

class UserRepo(Protocol):
    def get_by_id(self, user_id: str) -> Optional[dict]: ...

class SqlAlchemyUserRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: str) -> Optional[dict]:
        # map ORM entity -> dict for domain purity
        u = self.session.get(User, user_id)
        return None if not u else {"id": u.id, "email": u.email.lower()}
```
