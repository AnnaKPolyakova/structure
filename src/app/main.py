import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from black import Any
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.app.core.config import settings
from src.app.db.postgres import postgres_provider
from src.app.db.redis import redis_provider

logging.basicConfig(level=settings.APP_LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # ---------- STARTUP ----------

    # Postgres init
    try:
        await postgres_provider.connect()
        logger.info("Postgres initialized")
    except Exception as e:
        logger.exception("Postgres init failed: %s", e)

    # Redis init
    await redis_provider.connect()
    await redis_provider.ping()
    logger.info("Redis initialized")
    yield

    # ---------- SHUTDOWN ----------
    try:
        await postgres_provider.close()
        logger.info("Postgres closed")
    except Exception:
        logger.exception("Error during Postgres shutdown")

    if redis_provider.get_redis() is not None:
        await redis_provider.disconnect()
        logger.info("Redis closed")


app: FastAPI = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


@app.get("/ping")  # type: ignore[misc]
async def ping() -> dict[str, Any]:
    result: dict[str, Any] = {}

    # Redis
    try:
        if await redis_provider.ping():
            result["redis_ping"] = "pong"
        else:
            result["redis_ping"] = "fail"
    except Exception as e:
        result["redis_error"] = str(e)

    # Postgres
    try:
        if await postgres_provider.ping():
            result["postgres_ping"] = "pong"
        else:
            result["postgres_ping"] = "fail"
    except Exception as e:
        result["postgres_error"] = str(e)

    return result
