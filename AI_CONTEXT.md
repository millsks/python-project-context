# AI Context (Vendor-Neutral)

This file provides context for AI coding assistants (GitHub Copilot, Cursor, Cline, Aider, Devin, etc.) working on Python projects.

## Project Facts

**Quick Reference:**
- **Python**: >=3.11, <3.13
- **Project Layout**: `src/` for code, `tests/` for tests, `features/` for BDD, `e2e/` for Playwright
- **Formatter**: Ruff (line-length 100, includes import sorting)
- **Linter**: Ruff (E, F, I, B, UP, ANN, SIM)
- **Type Checker**: MyPy (strict-ish mode)
- **Test Runner**: pytest (unit/integration), behave (BDD), Playwright (E2E)
- **Task Runner**: Pixi (`pixi.toml`)
- **Local DB**: SQLite (`.data/dev.db`)
- **Prod DB**: PostgreSQL via `DATABASE_URL` env var

**Standard Commands:**
```bash
pixi run fmt          # Format code (ruff format + auto-fix)
pixi run fmt-check    # Check formatting (CI-safe, no mutations)
pixi run lint         # Lint code (ruff check)
pixi run mypy         # Type check
pixi run test         # Run pytest
pixi run bdd          # Run behave tests
pixi run e2e          # Run Playwright tests
pixi run ci           # All checks (fmt-check, mypy, test)
```

## Coding Style

### General Principles
- Follow PEP 8 strictly: spaces over tabs, 100-char line length
- Prefer readability and explicitness over brevity; avoid clever one-liners
- Small, single-purpose functions; return early when logic is clear
- Type hints everywhere using `from __future__ import annotations`
- Google-style docstrings for all public APIs

### Python Specifics
- **Naming**: `snake_case` for variables/functions, `PascalCase` for classes, `SCREAMING_SNAKE_CASE` for constants
- **Data Models**: Use `dataclasses.dataclass` or Pydantic
- **Paths**: Use `pathlib.Path` over `os.path`
- **Logging**: Structured logging with `structlog` or stdlib `logging` with extras
- **SQLAlchemy**: Use 2.0 style with sessionmaker per request/task
- **Module Organization**: Keep modules focused by domain; avoid "utils" grab-bags

### Docstring Example
```python
def fetch_active_user(user_id: str, session: Session) -> Optional[dict]:
    """
    Fetch an active user by ID.

    Args:
        user_id: The UUID of the user.
        session: SQLAlchemy session for database access.

    Returns:
        Dict with user fields if found and active, else None.

    Raises:
        UserServiceError: On repository failures.
    """
    # implementation
```

## Project Structure

```
src/<package_name>/     # Library/app code
tests/                  # Unit/integration tests (pytest)
features/               # BDD specs (behave)
e2e/                    # Playwright E2E tests
scripts/                # CLI scripts (idempotent)
examples/               # Runnable patterns/templates
```

## Error Handling & Security

### Error Handling
- Use custom exceptions per module/package for domain errors
- Never swallow exceptions silently; always log with structured context
- Validate inputs at boundaries; sanitize outputs for logs

### Security
- No secrets in code; use env vars or secret manager (see `.env.example`)
- Use parameterized queries/ORM; never string-concatenate SQL
- Add timeouts/retries for I/O with exponential backoff

## Database & I/O

### Database URLs
- **Local dev**: `sqlite:///./.data/dev.db`
- **Test**: `sqlite+pysqlite:///:memory:`
- **Prod**: `postgresql+psycopg://user:pass@host:5432/dbname` via `DATABASE_URL` env var

### Patterns
- Abstract DB behind repository interface; inject engine/session
- Use SQLAlchemy 2.0 style with proper session management
- Migrations via Alembic; do not import models at migration runtime unnecessarily

### Repository Pattern Example
```python
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

## Testing Standards

### Test Layers
- **Unit (pytest)**: Pure, fast, mock external boundaries
- **Integration (pytest)**: DB (SQLite/Postgres), filesystem, HTTP test servers
- **BDD (behave)**: User-facing behaviors in business language
- **E2E (Playwright)**: Critical paths only; fast and flaky-resistant

### Pytest Conventions
- Tests in `tests/` named `test_*.py` or `*_test.py`
- **AAA pattern**: Arrange-Act-Assert; one logical assertion group per test
- Use fixtures in `tests/conftest.py` for session, client, temp dirs
- Parametrize for edge cases; avoid loops in tests
- Mocks only for external boundaries (HTTP, DB, FS)

### DB Test Fixtures
- Local: ephemeral SQLite (file or in-memory) with migrations applied
- Provide a `session` fixture that rolls back between tests

### Behave (BDD)
- `.feature` files under `features/`
- Steps in `features/steps/`; keep reusable and declarative
- Map steps to domain language, not UI specifics

### Playwright (E2E)
- Tests in `e2e/` with fixtures for auth, baseURL
- Record trace/video on failure only; headless by default in CI
- Seed data via API or DB fixture; clean up after

## Code Patterns We Prefer

### Dependency Injection
- Inject services (DB, HTTP clients, time) rather than importing globally
- Pure domain functions; thin adapters for I/O
- Configuration via env vars with typed config loader

### Example Service Function
```python
from typing import Protocol

class UserRepo(Protocol):
    def get_by_id(self, user_id: str) -> Optional[dict]: ...

async def get_user_profile(user_id: str, repo: UserRepo, logger) -> Optional[dict]:
    if not user_id:
        logger.warning("Missing user_id")
        return None
    user = repo.get_by_id(user_id)
    if not user:
        logger.info("User not found", extra={"user_id": user_id})
        return None
    return {"id": user["id"], "email": user["email"]}
```

## Anti-Patterns (Avoid)

- Large functions (>80 lines) or deep nesting (>2 levels)
- Side effects in constructors or at import time
- Global mutable state
- Mixing sync/async unless necessary and well-isolated
- String concatenation for SQL queries

## Related Files

For more detailed guidance, see:
- **PY_STYLE.md** - Python-specific style details
- **TESTING_GUIDE.md** - Testing conventions and commands
- **DB_GUIDE.md** - Database configuration
- **TOOLS_PREFERENCES.md** - Tooling commands
- **PROMPT_TEMPLATES.md** - Reusable prompts for AI assistants
- **pyproject.toml** - Tool configurations (Ruff, MyPy, pytest)
- **pixi.toml** - Tasks and dependencies

## Assistant-Specific Files

- **.cursorrules** - Cursor IDE context
- **.clinerules** - Cline/Claude Code context
- **.github/copilot-instructions.md** - GitHub Copilot context
