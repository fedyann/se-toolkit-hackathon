# Simple Dockerfile for the MindLog backend.
# Uses uv for dependency management (same as lab-8).

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
COPY requirements.txt .

# Install Python dependencies
RUN uv pip install --system -r requirements.txt

# Create the backend package directory and copy code into it
RUN mkdir -p /app/backend
COPY *.py /app/backend/

# Expose the port FastAPI listens on
EXPOSE 8000

# Run the server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
