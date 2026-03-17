from ..models import QAHistory
from utils.db_util import db_connection
from utils.logger import logger


@db_connection
def get_history_by_user_id(user_id: int, db=None):
    logger.debug(f"[Mapper] 查询用户 {user_id} QA历史")
    history = db.query(QAHistory).filter(QAHistory.user_id == user_id).order_by(QAHistory.create_time.desc()).all()

    return [
        {
            "qa_id": h.qa_id,
            "question": h.question,
            "answer": h.answer,
            "create_time": h.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        for h in history
    ]


@db_connection
def insert_history(user_id: int, question: str, answer: str, source_chunks="", similarity_scores="", db=None):
    logger.debug(f"[Mapper] 插入QA历史，用户：{user_id}")
    new_history = QAHistory(
        user_id=user_id,
        question=question,
        answer=answer,
        source_chunks=source_chunks,
        similarity_scores=similarity_scores
    )
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    return new_history.qa_id


@db_connection
def delete_history_by_user_id(user_id: int, db=None):
    logger.debug(f"[Mapper] 删除用户 {user_id} 全部QA历史")
    count = db.query(QAHistory).filter(QAHistory.user_id == user_id).delete()
    db.commit()
    return count