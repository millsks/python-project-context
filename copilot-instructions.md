# GitHub Copilot Instructions

This file provides concentrated context for GitHub Copilot when reviewing PRs and generating code suggestions on GitHub.com. For full details, see the root context files: COPILOT_CONTEXT.md, PY_STYLE.md, TESTING_GUIDE.md, and others.

---

## Coding Style & Standards

### General Principles
- Follow PEP 8 strictly: spaces over tabs, 100-char line length
- Prefer readability and explicitness over brevity; avoid clever one-liners
- Small, single-purpose functions; return early when logic is clear
- Type hints everywhere using `from __future__ import annotations`
- Google-style docstrings for all public APIs

### Python Specifics
- Use `dataclasses.dataclass` or Pydantic for data models
- Use `pathlib.Path` over `os.path`
- Structured logging with `structlog` or stdlib `logging` with extras
- SQLAlchemy 2.0 style: sessionmaker per request/task
- Keep modules focused by domain; avoid "utils" grab-bags

### Naming Conventions
- `camelCase` for variables
- `PascalCase` for types/classes
- `SCREAMING_SNAKE_CASE` for constants
- Descriptive verbs for functions: `get_`, `set_`, `compute_`, `validate_`, `transform_`

---

## Project Structure

```
src/<package_name>/     # Library/app code
tests/                  # Unit/integration tests (pytest)
features/               # BDD specs (behave)
e2e/                    # Playwright E2E tests
scripts/                # CLI scripts (idempotent)
examples/               # Runnable patterns/templates
```

---

## Error Handling & Security

### Error Handling
- Use custom exceptions per module/package for domain errors
- Never swallow exceptions silently; always log with structured context
- Validate inputs at boundaries; sanitize outputs for logs

### Security
- No secrets in code; use env vars or secret manager
- Use parameterized queries/ORM; never string-concatenate SQL
- Add timeouts/retries for I/O with exponential backoff

---

## Database & I/O

### Database URLs
- Local dev: `sqlite:///./.data/dev.db`
- Test: `sqlite+pysqlite:///:memory:`
- Prod: `postgresql+psycopg://user:pass@host:5432/dbname` via `DATABASE_URL` env var

### Patterns
- Abstract DB behind repository interface; inject engine/session
- Use SQLAlchemy 2.0 style with proper session management
- Migrations via Alembic; do not import models at migration runtime unnecessarily

### Example Repository Pattern
```python
from typing import Protocol, Optional
from sqlalchemy.orm import Session

class UserRepo(Protocol):
    def get_by_id(self, user_id: str) -> Optional[dict]: ...

class SqlAlchemyUserRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: str) -> Optional[dict]:
        u = self.session.get(User, user_id)
        return None if not u else {"id": u.id, "email": u.email.lower()}
```

---

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

### Example Pytest Fixture
```python
from __future__ import annotations
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

TEST_DB_URL = os.getenv("TEST_DATABASE_URL", "sqlite+pysqlite:///:memory:")

@pytest.fixture(scope="session")
def engine():
    eng = create_engine(TEST_DB_URL, future=True)
    # Apply migrations or create_all here
    yield eng
    eng.dispose()

@pytest.fixture()
def session(engine) -> Session:
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
```

---

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

---

## Anti-Patterns (Avoid)

- Large functions (>80 lines) or deep nesting (>2 levels)
- Side effects in constructors or at import time
- Global mutable state
- Mixing sync/async unless necessary and well-isolated
- String concatenation for SQL queries

---

## Tooling & Commands

### Pixi Tasks
- Format: `pixi run fmt` (Black + isort)
- Lint: `pixi run lint` (Ruff)
- Type check: `pixi run mypy`
- Test: `pixi run test` (pytest)
- BDD: `pixi run bdd` (behave)
- E2E: `pixi run e2e` (Playwright)
- All checks: `pixi run ci`

### Tool Configuration
- **Black**: line-length 100, target py311
- **isort**: profile=black, line_length 100
- **Ruff**: extend-select E,F,I,B,UP,ANN,SIM; ignore ANN101,ANN102
- **MyPy**: strict-ish (warn_return_any, disallow_untyped_defs, etc.)

---

## Docstring Example

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

---

## Environment

- Python: >=3.11
- Local DB: SQLite (`.data/dev.db`)
- Prod DB: Postgres via `DATABASE_URL` env var
- Task runner: Pixi (`pixi.toml`)

---

## Summary for PR Reviews

When reviewing code or generating suggestions:
1. Enforce PEP 8, type hints, and 100-char lines
2. Check for dependency injection and pure functions
3. Verify tests follow AAA pattern with proper fixtures
4. Ensure no secrets, SQL injection risks, or global state
5. Prefer small functions with early returns
6. Validate docstrings for public APIs

For complete context, see root files: COPILOT_CONTEXT.md, PY_STYLE.md, TESTING_GUIDE.md, TOOLS_PREFERENCES.md, DB_GUIDE.md.
