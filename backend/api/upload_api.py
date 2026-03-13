from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import ApiResponse
from ..service.upload_service import upload_document

router = APIRouter()

@router.post("/api/upload", response_model=ApiResponse)
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    doc_id = await upload_document(file, db)
    return ApiResponse(code=0, data={"doc_id": doc_id})