# backend/mapper/qa_mapper.py
from backend.models import DocumentChunk, QAHistory
from utils.db_util import db_connection

@db_connection
def list_all_document_chunks(db=None):
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