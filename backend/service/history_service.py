from sqlalchemy.orm import Session
from ..models import QAHistory

def get_qa_history(page: int, size: int, db: Session):
    skip = (page - 1) * size
    total = db.query(QAHistory).count()
    items = db.query(QAHistory).order_by(QAHistory.create_time.desc()).offset(skip).limit(size).all()

    return {
        "list": [
            {
                "id": i.id,
                "question": i.question,
                "answer": i.answer,
                "time": i.create_time.strftime("%Y-%m-%d %H:%M:%S")
            } for i in items
        ],
        "total": total
    }