# Use the official Python image as a base
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python - && \
    chmod +x $HOME/.poetry/bin/poetry && \
    ln -s $HOME/.poetry/bin/poetry /usr/local/bin/poetry

# Copy pyproject.toml and poetry.lock to leverage Docker cache
COPY ./pyproject.toml ./poetry.lock* /app/

# Install backend dependencies
RUN poetry install --no-root --no-dev

# Copy the rest of the application code
COPY ./src /app/src
COPY ./scripts /app/scripts
COPY ./alembic.ini /app/alembic.ini
COPY ./models /app/models # If pre-trained models exist, copy them

# Expose the port FastAPI runs on
EXPOSE 8000

# Run database migrations and then start the FastAPI application
# Using a custom entrypoint script to ensure migrations run before app starts
COPY ./start.sh /app/start.sh
RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]