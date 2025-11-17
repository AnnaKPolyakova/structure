## structure

Небольшой сервис на FastAPI с подключением к PostgreSQL и Redis. Предоставляет базовый /ping эндпоинт для проверки доступности зависимостей и готов к дальнейшему развитию (модели, миграции Alembic, Celery/Redis, Nginx).

### Стек
- **FastAPI** (Uvicorn)
- **SQLAlchemy/SQLModel** (async, `asyncpg`)
- **Redis** (async)
- **Pydantic Settings** для конфигурации
- **Alembic** для миграций
- **Docker Compose** для инфраструктуры (Postgres, Redis, Nginx)

### Структура проекта (основное)
`
src/app/
  core/          # конфиг и логирование
  db/            # Postgres/Redis клиенты
  models/        # SQLModel (база и сущности)
  api/           # точки расширения API
  main.py        # FastAPI приложение и /ping
tests/         # Тесты
alembic/         # миграции
docker-compose*.yml
Dockerfile
nginx/nginx.conf
`

### Требования
- Python 3.13+
- Poetry 2.x
- (опционально) Docker + Docker Compose

### Установка (локально, без Docker)
`bash
poetry install --no-root
`

### Переменные окружения
Проект читает `.env` (см. `src/app/core/config.py`).
Значения по умолчанию подставляются, но рекомендуется явно задать их, пример
в env_example

### Запуск приложения (локально)

`python3 -m src.app.__main__`

После запуска:
- Swagger UI: `http://localhost:8000/docs`
- OpenAPI: `http://localhost:8000/openapi.json`
- Здоровье сервисов: `GET http://localhost:8000/ping`

Пример ответа `/ping`:
`json
{
  "redis_ping": "pong",
  "postgres_ping": "pong"
}
`

### База данных и миграции (Alembic)
Инициализация (если потребуется):
`bash
alembic init alembic
`

Создать миграции:
`bash
alembic revision --autogenerate -m "add user"
`

Применить миграции:
`bash
alembic upgrade head
`

Обратите внимание: укажите корректный DSN/переменные окружения для
подключения к вашей БД (см. `.env`).

### Запуск инфраструктуры в Docker (Postgres/Redis)
Для локальной разработки достаточно поднять Postgres и Redis:
`docker compose -f docker-compose-local.yml up -d`

### Тесты
`pytest`

### Линтеры и форматирование
`black src test`
`mypy src tests`
`ruff check`

### Полезные ссылки по коду
- Конфигурация: `src/app/core/config.py`
- Инициализация БД/Redis:
`src/app/db/postgres.py`
`src/app/db/redis.py`
- Приложение: `src/app/main.py`

### Лицензия
MIT
