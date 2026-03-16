# backend/api/qa_api.py
from fastapi import APIRouter, Header, HTTPException
from ..schemas import ApiResponse, QAQuery
from ..service.qa_service import ask_question
from utils.jwt_util import get_current_user

router = APIRouter()

@router.post("/api/qa/ask", response_model=ApiResponse)
def qa_ask(
    query: QAQuery,
    authorization: str = Header(None)
):
    # 1. 校验 token
    if not authorization:
        raise HTTPException(status_code=401, detail="未提供token")

    try:
        token = authorization.split(" ")[1]
        user = get_current_user(token)
        user_id = user["user_id"]
    except:
        raise HTTPException(status_code=401, detail="token无效或已过期")

    # 2. 调用 service（绝对无 db！）
    answer, source = ask_question(query.question, user_id)

    return ApiResponse(code=0, data={
        "answer": answer,
        "source": source
    })