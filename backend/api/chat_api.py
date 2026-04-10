from fastapi import APIRouter, Header, Body
from backend.utils.logger import logger
from backend.schemas.api_response import ApiResponse
from backend.service.chat_service import create_new_chat, list_user_chats, update_chat_title_service
from backend.utils.jwt_util import get_user_id_from_token
from backend.core.exceptions import UnauthorizedException

router = APIRouter()


# 获取对话列表
@router.get("/api/chat/list", response_model=ApiResponse)
def get_chat_list(authorization: str = Header(None)):
    logger.info("=== 获取用户对话列表 ===")
    if not authorization:
        raise UnauthorizedException()

    user_id = get_user_id_from_token(authorization)
    logger.info(f"用户 {user_id} 获取对话列表")

    chats = list_user_chats(user_id)

    return ApiResponse(code=0, data={
        "chats": [
            {
                "chat_id": c["chat_id"],
                "title": c["title"],
                "create_time": c["create_time"]
            } for c in chats
        ]
    })


# 新建对话
@router.post("/api/chat/new", response_model=ApiResponse)
def create_chat(authorization: str = Header(None)):
    logger.info("=== 新建对话 ===")
    if not authorization:
        raise UnauthorizedException()

    user_id = get_user_id_from_token(authorization)

    chat = create_new_chat(user_id)
    logger.info(f"用户 {user_id} 新建对话成功，chat_id = {chat['chat_id']}")

    return ApiResponse(code=0, data={"chat_id": chat["chat_id"]})


# 删除对话
@router.delete("/api/chat/delete/{chat_id}", response_model=ApiResponse)
def delete_chat(chat_id: int, authorization: str = Header(None)):
    logger.info(f"=== 删除对话：chat_id = {chat_id} ===")
    if not authorization:
        raise UnauthorizedException()

    user_id = get_user_id_from_token(authorization)
    logger.info(f"用户 {user_id} 申请删除对话 {chat_id}")

    # ✅ 关键修复：避免覆盖函数名
    from backend.service.chat_service import delete_chat as delete_chat_func, delete_qa_by_chat

    delete_chat_func(chat_id, user_id)
    delete_qa_by_chat(chat_id, user_id)

    logger.info(f"对话 {chat_id} 删除成功")
    return ApiResponse(code=0, msg="删除成功")


# 重命名对话
@router.post("/api/chat/rename/{chat_id}", response_model=ApiResponse)
def rename_chat(
        chat_id: int,
        title: str = Body(..., embed=True),
        authorization: str = Header(None)
):
    logger.info(f"=== 对话重命名：chat_id={chat_id}, 新标题={title} ===")
    if not authorization:
        raise UnauthorizedException()

    user_id = get_user_id_from_token(authorization)

    update_chat_title_service(chat_id, user_id, title)

    logger.info(f"用户 {user_id} 重命名成功 → {title}")
    return ApiResponse(code=0, msg="重命名成功")