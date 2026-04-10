from backend.models.document import Document
from backend.models.document_chunk import DocumentChunk
from backend.utils.db_util import db_connection
from backend.utils.orm_to_dict_util import to_dict
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
    db.flush()
    db.commit()

    # 自动转字典（替代手写）
    return to_dict(doc)


@db_connection
def batch_insert_chunks(chunk_data_list: list[dict], db=None):
    logger.debug(f"[Mapper] 批量插入分块，数量：{len(chunk_data_list)}")

    chunk_items = [
        DocumentChunk(
            doc_id=data["doc_id"],
            chunk_text=data["chunk_text"],
            chunk_embedding=data["chunk_embedding"],
            chunk_index=data["chunk_index"]
        )
        for data in chunk_data_list
    ]

    db.add_all(chunk_items)
    db.flush()
    db.commit()

    # 自动转换列表
    return to_dict(chunk_items)


# ======================
# 文档管理
# ======================
@db_connection
def list_user_documents(user_id: int, db=None):
    logger.debug(f"[Mapper] 查询用户 {user_id} 文档列表")

    docs = db.query(Document).filter(
        Document.user_id == user_id
    ).all()

    # 自动转换列表
    return to_dict(docs)


@db_connection
def delete_document(doc_id: int, user_id: int, db=None):
    logger.debug(f"[Mapper] 删除文档 {doc_id}，所属用户 {user_id}")

    doc = db.query(Document).filter(
        Document.doc_id == doc_id,
        Document.user_id == user_id
    ).first()

    if not doc:
        return False

    db.query(DocumentChunk).filter(
        DocumentChunk.doc_id == doc_id
    ).delete(synchronize_session=False)

    db.delete(doc)
    db.commit()

    return True


# ======================
# 查询工具
# ======================
@db_connection
def get_document_by_name(user_id: int, doc_name: str, db=None):
    logger.debug(f"[Mapper] 查询文档（按名称）：{doc_name}")

    doc = db.query(Document).filter(
        Document.user_id == user_id,
        Document.doc_name == doc_name
    ).first()

    # 自动转换
    return to_dict(doc)