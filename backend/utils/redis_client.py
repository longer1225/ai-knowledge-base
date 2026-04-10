import redis
from redis.exceptions import ConnectionError
from config import settings  # 后续可把 Redis 配置抽入配置文件

# 全局 Redis 客户端实例
_redis_client = None

def get_redis_client():
    """获取 Redis 客户端（单例）"""
    global _redis_client
    if _redis_client is None:
        try:
            _redis_client = redis.Redis(
                host="localhost",  # Redis 地址
                port=6379,         # 默认端口
                db=0,              # 数据库编号（0-15，默认用0）
                decode_responses=True,  # 自动把 bytes 转字符串
                socket_timeout=5   # 连接超时时间
            )
            # 测试连接
            _redis_client.ping()
            print("Redis 连接成功 ✅")
        except ConnectionError:
            raise Exception("Redis 连接失败！请检查 Redis 是否启动")
    return _redis_client

# 初始化客户端
redis_client = get_redis_client()