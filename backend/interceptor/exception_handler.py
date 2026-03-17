from fastapi import Request
from fastapi.responses import JSONResponse
from config import ENV_MODE
from backend.exceptions import BusinessException

async def global_exception_handler(request: Request, exc: Exception):
    # 1. 业务异常（我们自己抛的）
    if isinstance(exc, BusinessException):
        return JSONResponse(
            status_code=200,
            content={
                "code": exc.code,
                "msg": exc.msg,
                "data": None
            }
        )

    # 2. 系统异常
    if ENV_MODE == "dev":
        err_msg = str(exc)
    else:
        err_msg = "服务器繁忙，请稍后再试"

    return JSONResponse(
        status_code=200,
        content={
            "code": 500,
            "msg": err_msg,
            "data": None
        }
    )