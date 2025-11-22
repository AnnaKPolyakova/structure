import logging
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.app.core.config import settings

logger = logging.getLogger(__name__)


class PgConnector:
    def __init__(self, url: str, autoflush: bool = True):
        self._url = url
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = None
        self._autoflush = autoflush

    async def connect(self) -> None:
        try:
            self._engine = create_async_engine(
                self._url,
                pool_pre_ping=True,
                future=True,
            )
            self._sessionmaker = async_sessionmaker(
                bind=self._engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=self._autoflush,
            )
            logger.info("Postgres initialized")
        except Exception as e:
            logger.exception("Postgres init failed: %s", e)

    async def ping(self) -> bool | None:
        if self._engine is None:
            return False
        try:
            async with self._engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            raise RuntimeError(f"Postgres ping failed: {e}") from e

    async def close(self) -> None:
        if self._engine is not None:
            try:
                await self._engine.dispose()
            except Exception:
                logger.exception("Error during Postgres shutdown")


postgres_provider: PgConnector | None = None


def get_postgres_provider(test: bool = False) -> PgConnector:
    global postgres_provider  # noqa: PLW0603
    if test:
        postgres_provider = PgConnector(url=settings.POSTGRES_TEST_URL)
    else:
        postgres_provider = PgConnector(url=settings.POSTGRES_URL)
    return postgres_provider


async def get_db() -> AsyncGenerator[PgConnector | None]:
    yield postgres_provider
