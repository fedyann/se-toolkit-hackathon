# MindLog — Development Plan

## Version 1: Core Feature (Must Work End-to-End)

### Goal
A single-page web app where users can log a mood and negative thought,
get AI-powered distortion analysis + reframe, and see past entries.

### Backend
- [x] `POST /api/entries` — accepts `mood` (int) + `thought` (text), calls
  Qwen LLM, saves result to PostgreSQL, returns the full entry with
  distortion + reframe
- [x] `GET /api/entries` — returns all past entries, newest first
- [x] PostgreSQL table: `entries` (id, mood, thought, distortion, reframe,
  created_at)
- [x] LLM prompt: system prompt instructs Qwen to return strict JSON with
  `distortion` and `reframe` fields
- [x] Error handling: if LLM returns invalid JSON, return a fallback response

### Frontend
- [x] Mood slider (1–10) with live display
- [x] Text input for the negative thought
- [x] Submit button that calls `POST /api/entries`
- [x] Response area showing distortion name + reframe
- [x] List of past entries below the form

### Infrastructure
- [x] Docker Compose: backend, postgres, caddy
- [x] Caddy reverse proxy: serves frontend at `/`, proxies `/api` to backend
- [x] Port 42002 exposed externally

---

## Version 2: Dashboard

### Goal
A second page showing emotional patterns over time with charts and an
AI-generated weekly summary.

### New Backend Endpoints
- [x] `GET /api/dashboard` — returns:
  - `mood_over_time`: list of `{date, mood}` for the last 30 days
  - `distortion_counts`: dict of distortion name → count
  - `last_7_entries`: the 7 most recent entries (for summary context)
- [x] `POST /api/summary` — accepts last 7 entries, returns AI-generated
  summary paragraph ("Based on these entries, what patterns do you notice?")

### New Frontend
- [x] `dashboard.html` with:
  - Line chart of mood over time (Chart.js from CDN)
  - Horizontal bar chart of distortion frequency
  - AI summary paragraph
  - Emotion Weather visualization
  - Mood Pet with dynamic expressions
  - Micro Wins achievement cards
  - Insight Whispers section

### Notes
- All Version 2 endpoints are implemented and functional in `backend/main.py`.
- The `dashboard.html` file includes Chart.js integration, animated visualizations,
  and a complete UI matching the main journal page design.

---

## Timeline (3 Days)

| Day | Tasks                                    |
|-----|------------------------------------------|
| 1   | Version 1 complete — all files written, Docker Compose working, end-to-end test passing |
| 2   | Version 2 dashboard — charts, summary, polish UI |
| 3   | Testing, bug fixes, README, final submission prep |
