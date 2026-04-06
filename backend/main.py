"""MindLog — CBT Thought Journal API (FastAPI)."""

import logging
from datetime import datetime, date

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select
from sqlmodel.sql.expression import SelectOfScalar

from backend.database import init_db, get_session
from backend.models import Entry
from backend.schemas import (
    EntryCreate,
    EntryResponse,
    AnalysisResponse,
    DashboardResponse,
    SummaryResponse,
)
from backend.ai import analyze_thought

# Configure basic logging.
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="MindLog", description="CBT Thought Journal API", version="0.1.0")

# Allow all origins for development — tighten this in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Create database tables when the server starts."""
    init_db()
    logger.info("Database initialized.")


# ---------------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------------

@app.post("/api/entries", response_model=EntryResponse)
def create_entry(payload: EntryCreate, session=Depends(get_session)):
    """
    Accept a mood + thought, analyze it with the LLM, save to DB, return result.
    This is the main Version 1 endpoint.
    """
    # Call the AI to identify distortion and generate a reframe.
    analysis = analyze_thought(payload.thought)

    # Create and persist the entry.
    entry = Entry(
        mood=payload.mood,
        thought=payload.thought,
        distortion=analysis["distortion"],
        reframe=analysis["reframe"],
    )
    session.add(entry)
    session.commit()
    session.refresh(entry)

    logger.info(f"Entry created: id={entry.id}, distortion={analysis['distortion']}")
    return entry


@app.get("/api/entries", response_model=list[EntryResponse])
def list_entries(session=Depends(get_session)):
    """Return all past journal entries, newest first."""
    stmt = select(Entry).order_by(Entry.created_at.desc())
    return session.exec(stmt).all()


# ---------------------------------------------------------------------------
# Version 2 — Dashboard endpoints
# ---------------------------------------------------------------------------

@app.get("/api/dashboard", response_model=DashboardResponse)
def get_dashboard(session=Depends(get_session)):
    """
    Return data for the dashboard page:
    - mood_over_time: list of {date, mood} for the last 30 days
    - distortion_counts: dict of distortion name → count
    - last_7_entries: the 7 most recent entries (for the weekly summary)
    """
    # Get all entries.
    stmt = select(Entry).order_by(Entry.created_at.desc())
    all_entries = session.exec(stmt).all()

    # Mood over time — group by date, take the average mood per day.
    mood_map: dict[date, list[int]] = {}
    for e in all_entries:
        day = e.created_at.date()
        mood_map.setdefault(day, []).append(e.mood)

    mood_over_time = [
        {"date": d.isoformat(), "mood": round(sum(moods) / len(moods), 1)}
        for d, moods in sorted(mood_map.items(), reverse=True)[:30]
    ]

    # Distortion counts.
    distortion_counts: dict[str, int] = {}
    for e in all_entries:
        distortion_counts[e.distortion] = distortion_counts.get(e.distortion, 0) + 1

    # Last 7 entries for the weekly summary context.
    last_7 = all_entries[:7]

    return DashboardResponse(
        mood_over_time=mood_over_time,
        distortion_counts=distortion_counts,
        last_7_entries=[EntryResponse.model_validate(e) for e in last_7],
    )


@app.post("/api/summary", response_model=SummaryResponse)
def generate_summary(payload: list[EntryResponse]):
    """
    Accept a list of recent entries and return an AI-generated weekly summary.
    The LLM is prompted to notice patterns in the entries.
    """
    # Build a text summary of the entries to send to the LLM.
    entries_text = "\n".join(
        f"- Mood: {e.mood}/10, Thought: {e.thought}, Distortion: {e.distortion}"
        for e in payload
    )

    prompt = (
        f"Here are recent CBT journal entries:\n{entries_text}\n\n"
        "Based on these entries, what patterns do you notice? "
        "Write a short, supportive summary (2-4 sentences). "
        "Be gentle and encouraging. Do NOT include any JSON or special formatting — "
        "just plain text."
    )

    try:
        from backend.ai import analyze_thought_raw

        response = analyze_thought_raw(prompt, is_summary=True)
        return SummaryResponse(summary=response)

    except Exception as e:
        logger.error(f"Summary generation failed: {e}")
        return SummaryResponse(
            summary="We couldn't generate a summary right now. "
                    "Keep logging your thoughts — patterns will become clearer over time."
        )
