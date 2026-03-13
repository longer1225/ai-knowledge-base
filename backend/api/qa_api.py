from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import QAQuery, ApiResponse
from ..service.qa_service import ask_question

router = APIRouter()

@router.post("/api/qa", response_model=ApiResponse)
def qa(query: QAQuery, db: Session = Depends(get_db)):
    answer, source = ask_question(query.question, db)
    return ApiResponse(code=0, data={"answer": answer, "source": source})