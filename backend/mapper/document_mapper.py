from backend.models.document import Document
from backend.models.document_chunk import DocumentChunk
from backend.utils.db_util import db_connection
from backend.utils.logger import logger


# ======================
# Upload 相关
# ======================
@db_connection
def insert_document(
        user_id: int,
        doc_name: str,
        doc_type: str,
        file_size: int,
        status: str = "processed",
        db=None
):
    logger.debug(f"[Mapper] 插入文档：{doc_name}")
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
    logger.debug(f"[Mapper] 批量插入分块，数量：{len(chunk_items)}")
    db.add_all(chunk_items)
    db.commit()


# ======================
# 文档管理
# ======================
@db_connection
def list_user_documents(user_id: int, db=None):
    logger.debug(f"[Mapper] 查询用户 {user_id} 文档列表")
    return db.query(Document).filter(Document.user_id == user_id).all()


@db_connection
def delete_document(doc_id: int, user_id: int, db=None):
    logger.debug(f"[Mapper] 删除文档 {doc_id}，所属用户 {user_id}")

    # 先删除分块
    db.query(DocumentChunk).filter(DocumentChunk.doc_id == doc_id).delete()

    # 再删除文档
    doc = db.query(Document).filter(
        Document.doc_id == doc_id,
        Document.user_id == user_id
    ).first()

    if doc:
        db.delete(doc)
        db.commit()
        return True
    return False