from ..models import QAHistory, DocumentChunk
from utils.db_util import db_connection
from utils.logger import logger


# ====================== 【原有必备功能】全部保留 ======================
@db_connection
def list_all_document_chunks(db=None):
    logger.debug("[Mapper] 查询所有文档切片")
    return db.query(DocumentChunk).all()


@db_connection
def insert_qa_history(
    user_id: int,
    question: str,
    answer: str,
    source_chunks="",
    similarity_scores="",
    chat_id: int = None,
    db=None
):
    logger.debug(f"[Mapper] 插入QA历史，用户：{user_id}，窗口：{chat_id}")
    new_history = QAHistory(
        user_id=user_id,
        question=question,
        answer=answer,
        source_chunks=source_chunks,
        similarity_scores=similarity_scores,
        chat_id=chat_id
    )
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    return new_history.qa_id


# ====================== 多窗口：按窗口查询历史 ======================
@db_connection
def get_history_by_chat_id(user_id: int, chat_id: int, db=None):
    logger.debug(f"[Mapper] 查询用户 {user_id} 窗口 {chat_id} 历史")
    history = db.query(QAHistory)\
        .filter(
            QAHistory.user_id == user_id,
            QAHistory.chat_id == chat_id
        )\
        .order_by(QAHistory.create_time.desc())\
        .all()

    return [
        {
            "qa_id": h.qa_id,
            "question": h.question,
            "answer": h.answer,
            "create_time": h.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        for h in history
    ]


# ====================== 原有：查询用户全部历史 ======================
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


# ====================== 原有：删除用户历史 ======================
@db_connection
def delete_history_by_user_id(user_id: int, db=None):
    logger.debug(f"[Mapper] 删除用户 {user_id} 全部QA历史")
    count = db.query(QAHistory).filter(QAHistory.user_id == user_id).delete()
    db.commit()
    return count