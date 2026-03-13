from pydantic import BaseModel
from typing import Optional, Dict

class QAQuery(BaseModel):
    question: str

class ApiResponse(BaseModel):
    code: int
    msg: str = "成功"
    data: Optional[Dict] = None