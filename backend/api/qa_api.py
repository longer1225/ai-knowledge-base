from fastapi import APIRouter, Header
from starlette.responses import StreamingResponse
import asyncio

from backend.schemas.qa_query import QAQuery
from ..service.qa_service import ask_question_stream
from backend.utils.jwt_util import get_current_user
from backend.core.exceptions import UnauthorizedException
from backend.utils.logger import logger

from backend.config.backend_base_settings import ENV_MODE

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

@router.post("/api/qa/ask", response_class=StreamingResponse)
async def qa_ask(
    query: QAQuery,
    authorization: str = Header(None)
):
    logger.info("[API] 收到问答请求：%s", query.question)
    user_id = get_current_user_id(authorization)
    chat_id = query.chat_id

    # ✅ 不管什么环境，都进入 service
    return StreamingResponse(ask_question_stream(query.question, user_id, chat_id))