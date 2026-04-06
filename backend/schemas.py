"""Pydantic schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel


# --- Request schemas ---

class EntryCreate(BaseModel):
    """Payload for POST /api/entries — what the user submits."""
    mood: int
    thought: str


# --- Response schemas ---

class EntryResponse(BaseModel):
    """A single entry returned to the frontend."""
    id: int
    mood: int
    thought: str
    distortion: str
    reframe: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AnalysisResponse(BaseModel):
    """The AI analysis result returned alongside the saved entry."""
    distortion: str
    reframe: str


class DashboardResponse(BaseModel):
    """Data for the Version 2 dashboard page."""
    mood_over_time: list[dict]       # [{"date": "2025-01-01", "mood": 5}, ...]
    distortion_counts: dict[str, int]  # {"Catastrophizing": 3, ...}
    last_7_entries: list[EntryResponse]


class SummaryResponse(BaseModel):
    """AI-generated weekly summary text."""
    summary: str
