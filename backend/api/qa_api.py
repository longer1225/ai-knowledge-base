from fastapi import APIRouter, Header
from starlette.responses import StreamingResponse, JSONResponse

from backend.schemas.qa_query import QAQuery
from ..service.qa_service import ask_question_stream
from backend.utils.jwt_util import get_current_user
from backend.core.exceptions import UnauthorizedException
from backend.utils.logger import logger

# 🔥 导入配置，获取当前环境
from backend.config.backend_base_settings import BACKEND_CONFIG

router = APIRouter()


def get_current_user_id(authorization):
    if not authorization:
        raise UnauthorizedException()
    try:
        token = authorization.split(" ")[1]
        user = get_current_user(token)
        return user["user_id"]
    except Exception:
        raise UnauthorizedException("token无效或已过期")



@router.post("/api/qa/ask",response_class=StreamingResponse )
def qa_ask(
    query: QAQuery,
    authorization: str = Header(None)
):
    logger.info("[API] 收到问答请求：%s", query.question)
    user_id = get_current_user_id(authorization)

    # 🔥 🔥 🔥 强制打印当前环境（看后端控制台！）
    logger.info(f"【DEBUG】当前环境：{BACKEND_CONFIG.env}")

    if BACKEND_CONFIG.env == "dev":
        # 🟢 开发模式
        logger.info("【DEBUG】进入 DEV 模式，返回 JSON")
        return JSONResponse(...)
    else:
        # 🚀 生产模式
        logger.info("【DEBUG】进入 PROD 模式，返回流式")
        return StreamingResponse(...)