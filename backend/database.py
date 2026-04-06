"""Database connection and session management."""

import os

from sqlmodel import SQLModel, create_engine, Session

# Build the database URL from environment variables.
# Falls back to localhost if not set (useful for local dev).
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "mindlog")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)

# Synchronous engine — simpler to debug for beginners.
engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    """Create all tables defined in SQLModel models. Safe to call multiple times."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Yield a database session. Use as a FastAPI dependency."""
    with Session(engine) as session:
        yield session
