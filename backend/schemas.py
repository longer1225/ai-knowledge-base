from pydantic import BaseModel
from typing import Optional

# 请求模型
class QAQuery(BaseModel):
    question: str

# 响应模型
class ApiResponse(BaseModel):
    code: int
    data: Optional[dict] = None
    msg: Optional[str] = None