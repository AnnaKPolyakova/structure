from redis.asyncio import Redis, from_url

from src.app.core.config import settings

redis_client: Redis | None = None  # type: ignore[type-arg]


class RedisClient:
    def __init__(self, url: str):
        self.url = url
        self._redis: Redis | None = None  # type: ignore[type-arg]

    async def connect(self) -> None:
        self._redis = from_url(self.url)

    async def disconnect(self) -> None:
        if self._redis is not None:
            await self._redis.close()

    async def get_redis(self) -> Redis | None:  # type: ignore[type-arg]
        return self._redis

    async def ping(self) -> bool:
        if self._redis is None:
            return False
        try:
            return await self._redis.ping() is True
        except Exception:
            return False


redis_url: str = ("{protocol}://{host}:{port}").format(
    protocol=settings.REDIS_PROTOCOL,
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
)

redis_provider: RedisClient = RedisClient(redis_url)
