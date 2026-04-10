from pydantic import BaseModel

class QAQuery(BaseModel):
    question: str
    chat_id: int = None  # ✅ 加上这一行