from sqlalchemy.orm import Session
from passlib.context import CryptContext
from backend.mapper.user_mapper import get_user_by_username, create_mapper_user
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 密码加密
def get_password_hash(password: str) -> str:
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
def create_user(username: str, password: str):
    exists = get_user_by_username(username)
    if exists:
        raise HTTPException(status_code=400, detail="用户名已存在")

    hashed_pwd = get_password_hash(password)
    new_user = create_mapper_user(username, hashed_pwd)
    return new_user