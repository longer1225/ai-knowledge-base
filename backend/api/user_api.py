from fastapi import APIRouter
from pydantic import BaseModel
from backend.service.user_service import create_user, authenticate_user
from datetime import datetime, timedelta
from jose import jwt
from config.backend_base_settings import SECRET_KEY, ALGORITHM
from ..schemas import ApiResponse
from backend.exceptions import BusinessException, UnauthorizedException, ParamException
from utils.logger import logger

router = APIRouter(prefix="/api/user", tags=["用户管理"])

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register", response_model=ApiResponse)
def register(user: UserCreate):
    logger.info("[API] 用户注册：%s", user.username)

    if not user.username or not user.password:
        raise ParamException("用户名和密码不能为空")

    try:
        create_user(user.username, user.password)
        return ApiResponse(code=0, msg="注册成功")
    except BusinessException as e:
        raise e
    except Exception as e:
        logger.error(f"[API] 注册异常：{e}")
        raise BusinessException(msg="注册失败", code=500)


@router.post("/login", response_model=ApiResponse)
def login(user: UserLogin):
    logger.info("[API] 用户登录：%s", user.username)

    user_db = authenticate_user(user.username, user.password)
    if not user_db:
        raise UnauthorizedException("用户名或密码错误")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_db.username, "user_id": user_db.user_id},
        expires_delta=access_token_expires
    )

    return ApiResponse(code=0, data={
        "access_token": access_token,
        "token_type": "bearer",
        "username": user_db.username,
        "user_id": user_db.user_id
    }, msg="登录成功")