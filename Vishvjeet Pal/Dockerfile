# Multi-stage build for smaller image
FROM python:3.11-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip setuptools wheel
# Build wheels to speed up final image
RUN pip wheel --no-cache-dir -r requirements.txt -w /wheels

# Final image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install runtime deps (if any system libs needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels and install
COPY --from=builder /wheels /wheels
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/* || true

# Copy application
COPY . /app

# Create unprivileged user
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
ENV PORT=8000

# Use Uvicorn for production; consider gunicorn + uvicorn workers for heavy workloads
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
