from sqlalchemy.orm import Session
from passlib.context import CryptContext
from backend.mapper.user_mapper import get_user_by_username, create_mapper_user
from fastapi import HTTPException
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 密码加密

# 密码加密
def get_password_hash(password: str) -> str:
    password = password[:72]   # ⭐ bcrypt最大72字节
    return pwd_context.hash(password)

# 验证密码
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 登录逻辑
def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

# 注册逻辑
# 注册逻辑
import traceback

def create_user(username: str, password: str):
    try:

        exists = get_user_by_username(username)
        if exists:
            raise HTTPException(status_code=400, detail="用户名已存在")

        hashed_pwd = get_password_hash(password)

        new_user = create_mapper_user(username, hashed_pwd)

        return new_user

    except Exception as e:
        traceback.print_exc()   # ⭐ 打印真实错误
        raise e