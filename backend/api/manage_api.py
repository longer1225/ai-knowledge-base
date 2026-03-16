from fastapi import APIRouter, Header, HTTPException
from ..schemas import ApiResponse
from ..service.manage_service import get_user_documents, delete_user_document
from utils.jwt_util import get_current_user

router = APIRouter()

# 获取文档列表
@router.get("/api/manage", response_model=ApiResponse)
def get_documents(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="未提供token")

    try:
        token = authorization.split(" ")[1]
        user = get_current_user(token)

        # ======================================
        # 🔥 调试：打印出整个用户信息！！！
        print("🔥 解析出来的用户：", user)
        # =====================================


        user_id = user["user_id"]

    except:
        raise HTTPException(status_code=401, detail="token无效")

    docs = get_user_documents(user_id)
    return ApiResponse(code=0, data=docs)

# 删除文档
# manage_api.py 优化后
@router.delete("/api/manage/{doc_id}", response_model=ApiResponse)
def delete_document(doc_id: int, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="未提供token")

    try:
        token = authorization.split(" ")[1]
        user = get_current_user(token)
        user_id = user["user_id"]
    except:
        raise HTTPException(status_code=401, detail="token无效")

    try:
        delete_user_document(doc_id, user_id)
        return ApiResponse(code=0, msg="删除成功")
    except ValueError as e:
        # 捕获Service层的异常，返回400错误
        raise HTTPException(status_code=400, detail=str(e))