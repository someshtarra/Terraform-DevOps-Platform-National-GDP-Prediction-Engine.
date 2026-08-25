import json
from typing import Optional, Any
import redis.asyncio as redis
from app.core.config import settings
from app.core.logging import logger

redis_client: Optional[redis.Redis] = None


async def init_redis():
    global redis_client
    try:
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
            socket_timeout=5,
        )
        await redis_client.ping()
        logger.info("Connected to Redis successfully.")
    except Exception as e:
        logger.warning(f"Redis initialization failed: {e}. Running without Redis cache.")
        redis_client = None


async def get_cache(key: str) -> Optional[Any]:
    if not redis_client:
        return None
    try:
        val = await redis_client.get(key)
        if val:
            return json.loads(val)
    except Exception as e:
        logger.error(f"Redis get error for key {key}: {e}")
    return None


async def set_cache(key: str, value: Any, ttl: int = settings.CACHE_TTL_SECONDS):
    if not redis_client:
        return
    try:
        await redis_client.set(key, json.dumps(value), ex=ttl)
    except Exception as e:
        logger.error(f"Redis set error for key {key}: {e}")


async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()
        logger.info("Closed Redis connection.")
