from __future__ import annotations
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

TEST_DB_URL = os.getenv("TEST_DATABASE_URL", "sqlite+pysqlite:///:memory:")

@pytest.fixture(scope="session")
def engine():
    eng = create_engine(TEST_DB_URL, future=True)
    # TODO: apply migrations or create_all here for SQLite
    yield eng
    eng.dispose()

@pytest.fixture()
def session(engine) -> Session:
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
