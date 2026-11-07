# OER Hub — Кафедральный репозиторий образовательных ресурсов

Платформа для централизованного хранения, версионирования и публикации учебных материалов кафедры с интеграцией локального Git-сервера (Gitea).

## Архитектура и стек

- **Backend**: Python 3.12+, Django 5.2.*
- **Database**: SQLite (dev) / PostgreSQL 16 (prod)
- **Git Server**: Gitea
- **Async & Cache**: Redis 7
- **Dependencies & Tools**: uv, ruff

## Быстрый запуск

### 1. Настройка переменных окружения

```bash
cp .env.example .env
```

### 2. Запуск через Docker Compose

#### Секция разработки (dev: SQLite + hot-reload + DjDT):
```bash
docker compose --profile dev up --build
```

#### Продакшн секция (prod: PostgreSQL + Gunicorn):
```bash
docker compose --profile prod up --build
```

### 3. Локальный запуск через `uv`

```bash
uv sync --all-groups
cd oer_hub
uv run python manage.py migrate
uv run python manage.py create_admin
uv run python manage.py runserver
```

## Линтинг и тесты

```bash
uv run ruff check .
uv run ruff format --check .
cd oer_hub && uv run python manage.py test
```
