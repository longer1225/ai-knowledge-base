from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status

from backend.config.backend_base_settings import SECRET_KEY, ALGORITHM

# ==========================
# 全局配置
# ==========================
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ==========================
# 🔥 唯一创建 Token（结构只在这里定义）
# ==========================
def create_access_token(user_id: int, username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # ✅ Token 结构唯一在这里定义
    payload = {
        "user_id": user_id,
        "sub": username,
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ==========================
# 解析 Token 获取当前用户
# ==========================
def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")
        username = payload.get("sub")

        if user_id is None or username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效凭证"
            )
        return {
            "user_id": user_id,
            "username": username
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="登录已过期或无效"
        )


# ==========================
# 从 Authorization 头获取 user_id
# ==========================
def get_user_id_from_token(authorization: str):
    if not authorization:
        raise HTTPException(status_code=401, detail="未登录")

    token = authorization.split(" ")[-1]
    return get_current_user(token)["user_id"]