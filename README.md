# Blobbi — CBT Thought Journal

> A web app that helps users identify cognitive distortions in their negative thoughts and reframe them with AI assistance.

## Screenshots

<img width="3145" height="1733" alt="image" src="https://github.com/user-attachments/assets/bd88cbca-159e-44e1-8ce6-2990e1b04330" />

<img width="3154" height="1553" alt="image" src="https://github.com/user-attachments/assets/4da82e21-afe2-4b4a-ac1c-cde45dcf8183" />

<img width="3135" height="1649" alt="image" src="https://github.com/user-attachments/assets/3dceae44-2882-4daf-ae18-75ff443fe33c" />


## End Users

- Anyone practicing CBT (Cognitive Behavioral Therapy) techniques
- People who want to track their mood and thought patterns over time
- Students and individuals looking for a simple, private thought journal

## Problem

Negative thoughts often go unexamined. People experience cognitive distortions
(all-or-nothing thinking, catastrophizing, mind reading, etc.) without realizing
it, which can worsen mood and anxiety. Traditional CBT requires a therapist or
structured worksheets — there's no lightweight, always-available tool for
quick in-the-moment reframing.

## Solution

Blobbi lets users log a mood and a negative thought in seconds. An AI (Qwen
LLM) instantly identifies the cognitive distortion and offers a gentle,
compassionate reframe. Over time, the dashboard reveals emotional patterns
and distortion trends, helping users become more aware of their thinking
habits.

## Features

### Implemented (Version 1 + 2)

- ✅ Mood slider (1–10)
- ✅ Text input for negative thoughts
- ✅ AI-powered cognitive distortion identification
- ✅ AI-generated gentle reframe
- ✅ Persistent storage in PostgreSQL
- ✅ List of past entries with mood, thought, distortion, reframe, and date
- ✅ Dockerized deployment (FastAPI + PostgreSQL + Caddy)
- ✅ Reverse proxy on port 42002
- ✅ Dashboard page with mood-over-time line chart (Chart.js)
- ✅ Distortion breakdown bar chart
- ✅ Weekly AI summary ("What patterns do you notice?")
- ✅ `GET /api/dashboard` and `POST /api/summary` endpoints
- ✅ Emotion Weather visualization
- ✅ Mood Pet with dynamic expressions
- ✅ Micro Wins achievement system

## Tech Stack

| Component       | Technology                          |
|-----------------|-------------------------------------|
| Backend         | FastAPI (Python)                    |
| Database        | PostgreSQL 16                       |
| Frontend        | Vanilla HTML + CSS + JavaScript     |
| Reverse Proxy   | Caddy                               |
| LLM             | Qwen (via OpenAI-compatible API)    |
| Containerization| Docker Compose                      |
| Package Manager | uv (Python)                         |

## Usage Instructions

### Prerequisites

- Docker and Docker Compose installed
- Access to a Qwen Code API instance (port 42005)
- Ubuntu 24.04 VM (or similar Linux environment)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/fedyann/se-toolkit-hackathon.git
   cd se-toolkit-hackathon
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and set your QWEN_CODE_API_KEY
   ```

3. **Start all services:**
   ```bash
   docker compose up --build -d
   ```

4. **Open the app:**
   Navigate to `http://<your-vm-ip>:42002` in your browser.

5. **Log your first thought:**
   - Adjust the mood slider
   - Type a negative thought
   - Click "Analyze My Thought"
   - See the AI-identified distortion and reframe

### API Endpoints

| Method | Path             | Description                          |
|--------|------------------|--------------------------------------|
| POST   | `/api/entries`   | Create a new journal entry           |
| GET    | `/api/entries`   | List all past entries                |
| GET    | `/api/dashboard` | Get dashboard data (Version 2)       |
| POST   | `/api/summary`   | Generate weekly AI summary (V2)      |

## Deployment Instructions (Ubuntu 24.04)

1. **Install Docker:**
   ```bash
   curl -fsSL https://get.docker.com | sh
   sudo usermod -aG docker $USER
   # Log out and back in for group changes to take effect
   ```

2. **Clone and configure:**
   ```bash
   git clone https://github.com/fedyann/se-toolkit-hackathon.git
   cd se-toolkit-hackathon
   cp .env.example .env
   nano .env  # Set your QWEN_CODE_API_KEY
   ```

3. **If Qwen Code API is already running on the host** (from lab-8),
   you need to make it accessible from inside Docker. Add this to
   `docker-compose.yml` under the `backend` service environment:
   ```yaml
   - QWEN_API_BASE_URL=http://host.docker.internal:42005/v1
   ```
   And add `extra_hosts` to the backend service:
   ```yaml
   extra_hosts:
     - "host.docker.internal:host-gateway"
   ```

   **Alternatively**, if you want Docker Compose to start the Qwen API
   too, copy the `qwen-code-api/` directory from lab-8 into this repo
   and the existing `docker-compose.yml` will handle it.

4. **Start the app:**
   ```bash
   docker compose up --build -d
   ```

5. **Access the app** at `http://<vm-ip>:42002`.

6. **View logs:**
   ```bash
   docker compose logs -f backend
   ```

7. **Stop the app:**
   ```bash
   docker compose down
   ```

## Project Structure

```
se-toolkit-hackathon/
├── backend/
│   ├── main.py           # FastAPI app + routes
│   ├── models.py         # SQLModel database model
│   ├── database.py       # DB connection + session
│   ├── schemas.py        # Pydantic request/response schemas
│   ├── ai.py             # Qwen LLM call + JSON parsing
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile        # Backend container
├── frontend/
│   ├── index.html        # Journal entry page (Version 1)
│   ├── dashboard.html    # Dashboard with charts (Version 2)
│   └── style.css         # Shared styles
├── caddy/
│   └── Caddyfile         # Reverse proxy config
├── docker-compose.yml    # All services
├── .env.example          # Environment variables template
├── PLAN.md               # Development plan
└── README.md             # This file
```

## License

MIT License — see [LICENSE](LICENSE) for details.
