import redis
from redis.exceptions import RedisError
from backend.config.redis_config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD
from backend.utils.logger import logger


class RedisCache:
    def __init__(self):
        # 🔥 这里自动读配置
        self.client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD,
            decode_responses=False,
            socket_connect_timeout=1
        )

    def get(self, key):
        try:
            return self.client.get(key)
        except RedisError:
            return None

    def set(self, key, value, ex=300):
        try:
            self.client.setex(key, ex, value)
        except RedisError:
            pass

    def delete(self, key):
        try:
            self.client.delete(key)
        except RedisError:
            pass

    def incr(self, key: str):
        """让指定的 key 自增 1"""
        try:
            if self.redis_client:
                return self.redis_client.incr(key)
        except Exception as e:
            logger.error(f"Redis incr 异常: {e}")
            return None

redis_cache = RedisCache()