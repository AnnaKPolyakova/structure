from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from src.app.core.config import settings


class PgConnector:
    def __init__(self, url: str):
        self._url = url
        self._engine: AsyncEngine | None = None
        self._sessionmaker: sessionmaker | None = None

    async def connect(self) -> None:
        self._engine = create_async_engine(
            self._url,
            pool_pre_ping=True,
            future=True,
        )
        self._sessionmaker = sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        if self._sessionmaker is None:
            raise RuntimeError("Database is not initialized")

        async with self._sessionmaker() as session:
            yield session

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
            await self._engine.dispose()
            self._engine = None
            self._sessionmaker = None


postgres_url: str = (
    "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
).format(
    user=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    db=settings.POSTGRES_DB,
)

postgres_provider: PgConnector = PgConnector(postgres_url)
