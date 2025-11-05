# Database Guide

## URLs
- Local SQLite: `sqlite:///./.data/dev.db`
- Test SQLite (in-memory): `sqlite+pysqlite:///:memory:`
- Prod Postgres: `postgresql+psycopg://user:pass@host:5432/dbname` via `DATABASE_URL`

## Guidance
- Use SQLAlchemy engine/session factory injected into repos.
- Migrations (e.g., Alembic) run via task; do not import models at migration runtime unnecessarily.
- Never build SQL by string concatenation; use bound params/ORM.
