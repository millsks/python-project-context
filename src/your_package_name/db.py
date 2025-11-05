from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DEFAULT_SQLITE_URL = "sqlite:///./.data/dev.db"


def make_engine():
    url = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, future=True, pool_pre_ping=True, connect_args=connect_args)


def make_session_factory(engine=None):
    engine = engine or make_engine()
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
