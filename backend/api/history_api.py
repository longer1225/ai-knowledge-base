# backend/api/history_api.py
from fastapi import APIRouter, Header, HTTPException, Body
from ..schemas import ApiResponse
from ..service.history_service import get_user_qa_history, save_qa_history, clear_user_qa_history
from utils.jwt_util import get_current_user

router = APIRouter()


# 获取用户QA历史
@router.get("/api/history/qa", response_model=ApiResponse)
def api_get_qa_history(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="未提供token")
    try:
        token = authorization.split(" ")[1]
        user = get_current_user(token)
        user_id = user["user_id"]
    except Exception as e:
        raise HTTPException(status_code=401, detail="token无效")

    # 只调用Service，不碰DB/Mapper
    history = get_user_qa_history(user_id)
    return ApiResponse(code=0, data=history)


# 保存QA历史
@router.post("/api/history/qa", response_model=ApiResponse)
def api_save_qa_history(
        data: dict = Body(...),
        authorization: str = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="未提供token")
    try:
        token = authorization.split(" ")[1]
        user = get_current_user(token)
        user_id = user["user_id"]
    except Exception as e:
        raise HTTPException(status_code=401, detail="token无效")

    try:
        # 调用Service处理业务
        save_qa_history(
            user_id=user_id,
            question=data.get("question", ""),
            answer=data.get("answer", ""),
            source_chunks=data.get("source_chunks", ""),
            similarity_scores=data.get("similarity_scores", "")
        )
        return ApiResponse(code=0, msg="历史记录保存成功")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 清空QA历史
@router.delete("/api/history/qa", response_model=ApiResponse)
def api_clear_qa_history(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="未提供token")
    try:
        token = authorization.split(" ")[1]
        user = get_current_user(token)
        user_id = user["user_id"]
    except Exception as e:
        raise HTTPException(status_code=401, detail="token无效")

    clear_user_qa_history(user_id)
    return ApiResponse(code=0, msg="历史记录已清空")