from passlib.context import CryptContext

from backend.core.exceptions import BusinessException
from backend.mapper.user_mapper import get_user_by_username, create_mapper_user
from backend.utils.logger import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    password = password[:72]
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str):
    logger.debug(f"[Service] 认证用户：{username}")
    user = get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_user(username: str, password: str):
    logger.debug(f"[Service] 创建用户：{username}")

    exists = get_user_by_username(username)
    if exists:
        raise BusinessException(msg="用户名已存在", code=400)

    if len(password) < 6:
        raise BusinessException(msg="密码长度不能小于6位", code=400)

    hashed_pwd = get_password_hash(password)
    return create_mapper_user(username, hashed_pwd)