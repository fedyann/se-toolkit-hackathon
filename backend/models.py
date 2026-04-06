"""SQLModel database models for MindLog entries."""

from datetime import datetime

from sqlmodel import SQLModel, Field


class Entry(SQLModel, table=True):
    """A single CBT journal entry stored in PostgreSQL."""

    __tablename__ = "entries"

    id: int | None = Field(default=None, primary_key=True)
    mood: int = Field(ge=1, le=10, description="Mood rating from 1 to 10")
    thought: str = Field(description="The user's negative thought")
    distortion: str = Field(description="Identified cognitive distortion")
    reframe: str = Field(description="AI-generated gentle reframe")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When the entry was created")
