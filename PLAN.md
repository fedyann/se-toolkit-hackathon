# MindLog — Implementation Plan

## Product idea

A daily journal where you log your mood and a negative thought,
and AI identifies the cognitive distortion, reframes it,
and tracks your emotional patterns over time.

**End user:** Anyone dealing with stress or negative thinking patterns —
students, people curious about CBT techniques.

**Problem solved:** People rarely notice their own recurring negative
thought patterns. MindLog makes them visible and gently challenges
them using AI.

---

## Version 1 — Core check-in with AI analysis

**One-line goal:** User submits a mood rating and a thought,
AI identifies the cognitive distortion and offers a reframe,
result is saved and shown.

### Components

**Backend (FastAPI)**
- `POST /entries` — receives mood (1–10) and thought text,
  calls the AI, saves the result to the database, returns the analysis
- `GET /entries` — returns all past entries for the journal view

**Database (PostgreSQL)**
- One table: `entries`
  - `id`, `mood` (int), `thought` (text), `distortion` (text),
    `reframe` (text), `created_at` (timestamp)

**Frontend (HTML/JS)**
- A single page with:
  - A mood slider (1–10)
  - A text field: "What negative thought are you having?"
  - A submit button
  - A response section that shows the distortion name and the reframe
  - A simple list of past entries below

### What "done" looks like
- User fills in the form, submits, and sees a meaningful AI response
- The entry is saved and appears in the list below
- No crashes, no empty responses

---

## Version 2 — Dashboard and pattern tracking

**One-line goal:** Show the user their emotional patterns over time
with a mood chart and distortion breakdown.

### What is added on top of Version 1

**Backend**
- `GET /dashboard` — returns aggregated data:
  mood average per day, count of each distortion type

**Database**
- No schema changes — Version 2 reads the same `entries` table

**Frontend — new dashboard page**
- Mood over time: a simple line chart (Chart.js or plain SVG)
- Most frequent distortions: a small bar chart or ranked list
- A short AI-generated weekly summary:
  "This week you mostly experienced all-or-nothing thinking,
  often on low-mood days."

**Deployment**
- All services Dockerized: backend, postgres, frontend via Caddy
- Accessible at the VM's public IP

### What "done" looks like
- Dashboard page loads with real data from the database
- Mood chart shows at least the last 7 days
- Distortion breakdown shows which patterns appear most
- App is reachable from a browser without running anything locally
