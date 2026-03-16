from backend.models import Document, DocumentChunk
from utils.db_util import db_connection

@db_connection
def insert_document(
    user_id: int,
    doc_name: str,
    doc_type: str,
    file_size: int,
    status: str = "processed",
    db=None
):
    doc = Document(
        user_id=user_id,
        doc_name=doc_name,
        doc_type=doc_type,
        file_size=file_size,
        status=status
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

@db_connection
def batch_insert_chunks(chunk_items: list, db=None):
    db.add_all(chunk_items)
    db.commit()