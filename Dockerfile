FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_PROJECT_ENVIRONMENT="/usr/local"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

FROM base AS dev
RUN uv sync --all-groups --no-install-project
COPY . /app
WORKDIR /app/oer_hub
EXPOSE 8000
CMD python manage.py migrate \
 && python manage.py init_superuser \
 && python manage.py runserver 0.0.0.0:8000

FROM base AS prod
RUN uv sync --no-dev --no-install-project
COPY . /app
WORKDIR /app/oer_hub
EXPOSE 8000
CMD python manage.py migrate \
 && python manage.py init_superuser \
 && python manage.py collectstatic --no-input \
 && gunicorn oer_hub.wsgi:application --bind 0.0.0.0:8000 --workers 4
