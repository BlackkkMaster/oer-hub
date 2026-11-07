FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml README.md /app/

FROM base AS dev
RUN uv sync --all-groups
ENV PATH="/app/.venv/bin:$PATH"
COPY . /app
WORKDIR /app/oer_hub
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM base AS prod
RUN uv sync --no-dev
ENV PATH="/app/.venv/bin:$PATH"
COPY . /app
WORKDIR /app/oer_hub
RUN python manage.py collectstatic --noinput || true
EXPOSE 8000
CMD ["gunicorn", "oer_hub.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
