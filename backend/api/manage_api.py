from fastapi import APIRouter, Header
from backend.schemas.api_response import ApiResponse
from ..service.manage_service import get_user_documents, delete_user_document
from backend.utils.jwt_util import get_current_user
from backend.core.exceptions import BusinessException, UnauthorizedException
from backend.utils.logger import logger

router = APIRouter()


# 抽取通用用户解析方法
def get_current_user_id(authorization):
    if not authorization:
        raise UnauthorizedException()
    try:
        token = authorization.split(" ")[1]
        user = get_current_user(token)
        return user["user_id"]
    except Exception:
        raise UnauthorizedException("登录已过期，请重新登录")


@router.get("/api/manage", response_model=ApiResponse)
def get_documents(authorization: str = Header(None)):
    logger.info("[API] 获取用户文档列表")
    user_id = get_current_user_id(authorization)
    docs = get_user_documents(user_id)
    logger.info(f"[API] 用户 {user_id} 获取文档成功，数量：{len(docs)}")
    return ApiResponse(code=0, data=docs, msg="获取成功")


@router.delete("/api/manage/{doc_id}", response_model=ApiResponse)
def delete_document(doc_id: int, authorization: str = Header(None)):
    logger.info(f"[API] 删除文档，doc_id={doc_id}")
    user_id = get_current_user_id(authorization)

    try:
        delete_user_document(doc_id, user_id)
        logger.warning(f"[API] 用户 {user_id} 删除文档 {doc_id} 成功")
        return ApiResponse(code=0, msg="删除成功")
    except ValueError as e:
        logger.error(f"[API] 删除文档失败：{str(e)}")
        raise BusinessException(msg=str(e), code=400)