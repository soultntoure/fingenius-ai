#!/bin/sh
echo "Applying Alembic database migrations..."
# Check if alembic.ini and alembic/ are configured correctly
poetry run alembic upgrade head
echo "Database migrations applied."