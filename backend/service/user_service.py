from passlib.context import CryptContext
import json
from backend.utils.log_util import insert_operation_log
from backend.core.exceptions import BusinessException
from backend.mapper.user_mapper import get_user_by_username, create_mapper_user
from backend.utils.logger import logger
from backend.utils.redis_cache import redis_cache

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    password = password[:72]
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ======================
# 认证用户（纯字典版）
# ======================
def authenticate_user(username: str, password: str):
    logger.debug(f"[Service] 认证用户：{username}")

    cache_key = f"user:info:{username}"

    # 1. Redis 查询（直接返回字典）
    cache_data = redis_cache.get(cache_key)
    if cache_data:
        try:
            user_dict = json.loads(cache_data)
            if user_dict and verify_password(password, user_dict["password"]):
                return user_dict  # 直接返回字典
        except Exception as e:
            logger.warning(f"[Redis] 用户缓存解析失败: {e}")

    # 2. DB 查询（mapper 已经返回字典）
    user_dict = get_user_by_username(username)
    if not user_dict:
        return None

    # 3. 密码校验
    if not verify_password(password, user_dict["password"]):
        redis_cache.delete(cache_key)  # 🔥 清掉脏缓存
        return None

    # 4. 写入 Redis
    redis_cache.set(
        cache_key,
        json.dumps(user_dict, ensure_ascii=False),
        ex=300
    )
    # ======================
    # 记录登录日志
    # ======================
    insert_operation_log(
        user_id=user_dict["user_id"],
        operation="用户登录",
        module="用户模块",
        content=f"用户【{username}】登录系统"
    )

    return user_dict  # 直接返回字典


# ======================
# 创建用户（纯字典版）
# ======================
def create_user(username: str, password: str):
    logger.debug(f"[Service] 创建用户：{username}")

    exists = get_user_by_username(username)
    if exists:
        raise BusinessException(msg="用户名已存在", code=400)

    if len(password) < 6:
        raise BusinessException(msg="密码长度不能小于6位", code=400)

    hashed_pwd = get_password_hash(password)

    # Mapper 返回字典
    user_dict = create_mapper_user(username, hashed_pwd)

    # 清缓存
    cache_key = f"user:info:{username}"
    redis_cache.delete(cache_key)

    insert_operation_log(
        user_id=user_dict["user_id"],
        operation="用户注册",
        module="用户模块",
        content=f"新用户【{username}】注册"
    )

    return user_dict  # 直接返回字典