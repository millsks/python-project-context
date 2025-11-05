# Python Style

- PEP 8 with spaces, 100-char lines.
- Type hints everywhere; `from __future__ import annotations`.
- Prefer `dataclasses.dataclass` or Pydantic for data models.
- Use `pathlib.Path` over `os.path`.
- Logging: `structlog` or stdlib `logging` with structured extras.
- Use SQLAlchemy 2.0 style if using ORM; sessionmaker per request/task.
- Keep modules focused; avoid "utils" grab-bags. Name by domain.
- Public functions/classes have Google-style docstrings.

## Docstring Example
"""
Fetch an active user.

Args:
    user_id: The UUID of the user.

Returns:
    Dict with user fields if found and active, else None.

Raises:
    UserServiceError: On repository failures.
"""
