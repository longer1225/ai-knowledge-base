from pydantic import BaseModel
from typing import Optional, Any

# 请求模型
class QAQuery(BaseModel):
    question: str

# 响应模型（通用返回格式）
class ApiResponse(BaseModel):
    code: int
    data: Optional[Any] = None  # 👈 只改这里！支持列表、字典、数字、null
    msg: Optional[str] = None