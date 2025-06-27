#!/bin/sh
# Apply database migrations
sh /app/scripts/apply_migrations.sh

# Start the FastAPI application
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000