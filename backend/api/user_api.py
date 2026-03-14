from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.service.user_service import create_user, authenticate_user
from datetime import datetime, timedelta
from jose import jwt
from settings import SECRET_KEY, ALGORITHM

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


@router.post("/register")
def register(user: UserCreate):
    try:
        create_user(user.username, user.password)
        return {"code": 200, "msg": "注册成功"}
    except HTTPException as e:
        return {"code": e.status_code, "msg": e.detail}
    except Exception as e:
        return {"code": 500, "msg": f"注册失败：{str(e)}"}


@router.post("/login")
def login(user: UserLogin):
    user_db = authenticate_user(user.username, user.password)
    if not user_db:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_db.username, "user_id": user_db.user_id},
        expires_delta=access_token_expires
    )
    return {
        "code": 200,
        "access_token": access_token,
        "token_type": "bearer",
        "username": user_db.username,
        "user_id": user_db.user_id
    }