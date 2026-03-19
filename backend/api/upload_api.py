from fastapi import APIRouter, UploadFile, File, Request
from backend.schemas.api_response import ApiResponse
from ..service.upload_service import upload_document
from backend.utils.jwt_util import get_current_user
from backend.core.exceptions import BusinessException, UnauthorizedException
from backend.utils.logger import logger

router = APIRouter()


@router.post("/api/upload", response_model=ApiResponse)
async def upload(
        request: Request,
        file: UploadFile = File(...)
):
    logger.info("[API] 收到文件上传请求：%s", file.filename)

    # 兼容大小写请求头
    auth_header = request.headers.get("Authorization") or request.headers.get("authorization")
    if not auth_header:
        raise UnauthorizedException()

    try:
        # 解析 token
        token = auth_header.split(" ")[1] if " " in auth_header else auth_header
        user = get_current_user(token)
        user_id = user["user_id"]
    except Exception as e:
        logger.error("[API] Token 解析失败：%s", str(e))
        raise UnauthorizedException("token无效或已过期")

    # 执行业务
    try:
        doc_id = upload_document(file, user_id)
        logger.info("[API] 文件上传成功，doc_id=%s", doc_id)
        return ApiResponse(code=0, data={"doc_id": doc_id}, msg="上传成功")
    except BusinessException as e:
        raise e
    except Exception as e:
        logger.error("[API] 上传失败：%s", str(e))
        raise BusinessException(msg="文件处理失败", code=500)