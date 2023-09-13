import aioredis

import settings


async def get_redis_client():
    redis_client = await aioredis.from_url(settings.REDIS_DB_URL)
    return redis_client
