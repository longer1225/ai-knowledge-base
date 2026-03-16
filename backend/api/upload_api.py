from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from ..schemas import ApiResponse
from ..service.upload_service import upload_document
from utils.jwt_util import get_current_user

router = APIRouter()

@router.post("/api/upload", response_model=ApiResponse)
async def upload(
    request: Request,
    file: UploadFile = File(...)
):
    # 兼容 Authorization / authorization
    auth_header = request.headers.get("Authorization") or request.headers.get("authorization")

    print("【后端拿到的请求头】", auth_header)

    if not auth_header:
        raise HTTPException(status_code=401, detail="未提供token")

    try:
        # 支持两种格式
        # Authorization: Bearer token
        # Authorization: token
        if " " in auth_header:
            token = auth_header.split(" ")[1]
        else:
            token = auth_header

        user = get_current_user(token)
        user_id = user["user_id"]

    except Exception as e:
        print("【token解析错误】", e)
        raise HTTPException(status_code=401, detail="token无效或已过期")

    # 上传文档
    doc_id = upload_document(file, user_id)

    return ApiResponse(
        code=0,
        data={"doc_id": doc_id},
        msg="上传成功"
    )