from fastapi import APIRouter, Header, Body
from ..schemas import ApiResponse, QAQuery
from ..service.qa_service import ask_question
from utils.jwt_util import get_current_user
from backend.exceptions import BusinessException, UnauthorizedException
from utils.logger import logger

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


@router.post("/api/qa/ask", response_model=ApiResponse)
def qa_ask(
        query: QAQuery,
        authorization: str = Header(None)
):
    logger.info("[API] 收到问答请求：%s", query.question)
    user_id = get_current_user_id(authorization)

    answer, source = ask_question(query.question, user_id)
    logger.info("[API] 用户 %s 问答完成", user_id)

    return ApiResponse(code=0, data={
        "answer": answer,
        "source": source
    })