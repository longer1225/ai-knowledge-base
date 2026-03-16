from fastapi import Request, HTTPException
from utils.jwt_util import get_current_user
WHITE_LIST = [
    "/api/user/login",
    "/api/user/register",
    "/",
    "/docs",
    "/redoc",
    "/openapi.json"
]

async def auth_interceptor(request: Request, call_next):
    url = request.url.path

    # 白名单放行
    for w in WHITE_LIST:
        if url.startswith(w):
            return await call_next(request)

    # 检查 token
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="请先登录")

    token = auth_header[7:]
    get_current_user(token)

    return await call_next(request)