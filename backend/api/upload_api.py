from fastapi import APIRouter, UploadFile, File, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import ApiResponse
from ..service.upload_service import upload_document
from utils.jwt_util import get_current_user

router = APIRouter()


# 最终稳定版接口
@router.post("/api/upload", response_model=ApiResponse)
async def upload(
        file: UploadFile = File(...),
        authorization: str = Header(None),
        db: Session = Depends(get_db)
):
    # 1. 校验 token 是否存在
    if not authorization:
        raise HTTPException(status_code=401, detail="未提供token")

    try:
        token = authorization.split(" ")[1]
        user = get_current_user(token)
        user_id = user["user_id"]
    except:
        raise HTTPException(status_code=401, detail="token无效或已过期")

    # 2. 调用业务层
    doc_id = await upload_document(file, user_id, db)

    return ApiResponse(code=0, data={"doc_id": doc_id})