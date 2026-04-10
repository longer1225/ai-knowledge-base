from fastapi import APIRouter, Header, Body
from ..schemas.api_response import ApiResponse
from ..service.history_service import (
    get_user_qa_history,
    get_qa_history_by_chat,
    save_qa_history,
    clear_user_qa_history
)
from backend.utils.jwt_util import get_current_user
from backend.core.exceptions import BusinessException
from backend.utils.logger import logger

router = APIRouter()


def get_user_id(authorization):
    if not authorization:
        raise BusinessException(msg="请先登录", code=401)
    try:
        token = authorization.split(" ")[1]
        user = get_current_user(token)
        return user["user_id"]
    except Exception:
        raise BusinessException(msg="登录已过期，请重新登录", code=401)


# 原来：查全部
@router.get("/api/history/qa", response_model=ApiResponse)
def api_get_qa_history(authorization: str = Header(None)):
    logger.info("[API] 获取用户QA历史接口调用")
    user_id = get_user_id(authorization)
    data = get_user_qa_history(user_id)
    logger.info(f"[API] 用户 {user_id} 获取QA历史成功，数量：{len(data)}")
    return ApiResponse(code=0, data=data, msg="获取成功")


# 新增：按【窗口】查历史
@router.get("/api/history/chat/{chat_id}", response_model=ApiResponse)
def api_get_chat_history(chat_id: int, authorization: str = Header(None)):
    logger.info(f"[API] 获取窗口 {chat_id} 历史记录")
    user_id = get_user_id(authorization)
    data = get_qa_history_by_chat(user_id, chat_id)
    logger.info(f"[API] 窗口 {chat_id} 记录数：{len(data)}")
    return ApiResponse(code=0, data=data, msg="获取成功")


# 保存：支持 chat_id
@router.post("/api/history/qa", response_model=ApiResponse)
def api_save_qa_history(
    data: dict = Body(...),
    authorization: str = Header(None)
):
    logger.info("[API] 保存QA历史接口调用")
    user_id = get_user_id(authorization)
    question = data.get("question", "")
    answer = data.get("answer", "")
    chat_id = data.get("chat_id")

    save_qa_history(
        user_id=user_id,
        question=question,
        answer=answer,
        source_chunks=data.get("source_chunks", ""),
        similarity_scores=data.get("similarity_scores", ""),
        chat_id=chat_id
    )
    logger.info(f"[API] 用户 {user_id} 保存QA历史成功，窗口：{chat_id}")
    return ApiResponse(code=0, msg="保存成功")


@router.delete("/api/history/qa", response_model=ApiResponse)
def api_clear_qa_history(authorization: str = Header(None)):
    logger.info("[API] 清空QA历史接口调用")
    user_id = get_user_id(authorization)
    clear_user_qa_history(user_id)
    logger.warning(f"[API] 用户 {user_id} 已清空全部QA历史")
    return ApiResponse(code=0, msg="已清空历史记录")