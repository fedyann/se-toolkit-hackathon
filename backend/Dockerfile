# Dockerfile for the Blobbi backend. Build context is the repo root (it
# needs both backend/ and frontend/, since the backend also serves the
# static frontend). Uses uv for dependency management (same as lab-8).

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.12-slim-bookworm

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Install uv for fast pip installs
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy requirements first for better layer caching
COPY backend/requirements.txt backend/requirements.txt

# Install Python dependencies
RUN uv pip install --system -r backend/requirements.txt

# Create the backend package directory and copy code into it
RUN mkdir -p /app/backend
COPY backend/*.py /app/backend/
COPY frontend /app/frontend

# Expose the port FastAPI listens on
EXPOSE 8000

# Run the server. Railway injects $PORT at runtime; falls back to 8000
# for local docker-compose, which doesn't set it.
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
