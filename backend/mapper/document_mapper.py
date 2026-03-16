# 这是【唯一需要保留的 mapper】
# 包含了原来 upload_mapper + document管理 的所有功能
# 其他 mapper 都可以删了

from backend.models import Document, DocumentChunk
from utils.db_util import db_connection

# ======================
# 原来的 upload 相关
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

# ======================
# 文档管理（列表+删除）
# ======================
@db_connection
def list_user_documents(user_id: int, db=None):
    print("=" * 50)
    print("【调试】前端传过来的 user_id =", user_id)
    print("=" * 50)
    return db.query(Document).filter(Document.user_id == user_id).all()

@db_connection
def delete_document(doc_id: int, user_id: int, db=None):
    db.query(DocumentChunk).filter(DocumentChunk.doc_id == doc_id).delete()
    doc = db.query(Document).filter(
        Document.doc_id == doc_id,
        Document.user_id == user_id
    ).first()

    if doc:
        db.delete(doc)
        db.commit()
        return True
    return False