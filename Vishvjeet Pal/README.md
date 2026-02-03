# Task Tracker

Simple Task Tracker API (FastAPI).

## Rate Limiting 🔧
- Implemented as a lightweight in-memory middleware located at `core/utils/rate_limiter.py`.
- Default values (can be configured via environment variables):
  - `RATE_LIMIT_ENABLED` (default: `True`)
  - `RATE_LIMIT_REQUESTS` (default: `100`)
  - `RATE_LIMIT_WINDOW_SECONDS` (default: `60`)

> Note: The built-in limiter is intended for development/testing. For production use, replace it with a distributed store backed limiter (eg. Redis).

## Development

Install dependencies (in your virtualenv):

```bash
pip install -r requirements.txt
```

Run the app:

```bash
uvicorn main:app --reload
```

## Tests ✅

Run the test suite with:

```bash
pytest
```

The tests include `tests/test_rate_limit.py` which asserts per-route rate limiting via `/debug/ratelimit`.

## Customization

You can change limiter behavior via environment variables before starting the app, for example:

```bash
export RATE_LIMIT_REQUESTS=200
export RATE_LIMIT_WINDOW_SECONDS=60
export RATE_LIMIT_ENABLED=True
```

## Docker 🐳

A sample `Dockerfile` is included to build a production-ready image. Example commands:

```bash
# Build image
docker build -t task-tracker:latest .

# Run (map port 8000)
docker run -e RATE_LIMIT_ENABLED=true -p 8000:8000 task-tracker:latest
```

Notes:
- For production, use a managed database and set `DATABASE_URL` and `SECRET_KEY` environment variables.
- Run migrations inside the container (example):

```bash
# Start a one-off container and run alembic
docker run --rm -e DATABASE_URL="$DATABASE_URL" task-tracker:latest alembic upgrade head
```

> Tip: Replace the in-memory rate limiter with a Redis-backed one for clustered deployments.
