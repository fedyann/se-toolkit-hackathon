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
- [ ] `GET /api/dashboard` — returns:
  - `mood_over_time`: list of `{date, mood}` for the last 30 days
  - `distortion_counts`: dict of distortion name → count
  - `last_7_entries`: the 7 most recent entries (for summary context)
- [ ] `POST /api/summary` — accepts last 7 entries, returns AI-generated
  summary paragraph ("Based on these entries, what patterns do you notice?")

### New Frontend
- [ ] `dashboard.html` with:
  - Line chart of mood over time (Chart.js from CDN)
  - Horizontal bar chart of distortion frequency
  - AI summary paragraph

### Notes
- The `GET /api/dashboard` and `POST /api/summary` endpoints are already
  implemented in `backend/main.py` — they just need the frontend to use them.
- The `dashboard.html` file is already scaffolded with Chart.js integration.
- Version 2 is mostly a matter of testing and polishing the existing code.

---

## Timeline (3 Days)

| Day | Tasks                                    |
|-----|------------------------------------------|
| 1   | Version 1 complete — all files written, Docker Compose working, end-to-end test passing |
| 2   | Version 2 dashboard — charts, summary, polish UI |
| 3   | Testing, bug fixes, README, final submission prep |
