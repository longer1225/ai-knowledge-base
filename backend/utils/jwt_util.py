from jose import jwt, JWTError
from fastapi import HTTPException, status

from backend.config import SECRET_KEY, ALGORITHM


def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # ==============================
        # 🔥 完全匹配你登录代码的正确写法！
        # ==============================
        user_id = payload.get("user_id")    # 👈 从 user_id 拿
        username = payload.get("sub")       # 👈 从 sub 拿用户名

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

    # 专门获取 user_id 的函数
def get_user_id_from_token(authorization: str):
    if not authorization:
        raise HTTPException(status_code=401, detail="未登录")
    token = authorization.split(" ")[-1]
    return get_current_user(token)["user_id"]