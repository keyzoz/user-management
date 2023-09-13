import redis

from settings import REDIS_DB_URL


def get_redis_client():
    db = redis.StrictRedis.from_url(REDIS_DB_URL)
    try:
        yield db
    finally:
        db.close()
