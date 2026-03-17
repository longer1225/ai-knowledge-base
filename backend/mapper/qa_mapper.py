from backend.models import DocumentChunk, QAHistory
from utils.db_util import db_connection
from utils.logger import logger

@db_connection
def list_all_document_chunks(db=None):
    logger.debug("[Mapper] 获取所有文档分块")
    return db.query(DocumentChunk).all()

@db_connection
def insert_qa_history(
    user_id: int,
    question: str,
    answer: str,
    source_chunks: str,
    similarity_scores: str,
    db=None
):
    logger.debug(f"[Mapper] 保存QA历史，用户：{user_id}")
    history = QAHistory(
        user_id=user_id,
        question=question,
        answer=answer,
        source_chunks=source_chunks,
        similarity_scores=similarity_scores
    )
    db.add(history)
    db.commit()
    return history