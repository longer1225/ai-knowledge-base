from backend.mapper.document_mapper import list_user_documents, delete_document
from utils.logger import logger


def get_user_documents(user_id: int):
    logger.debug(f"[Service] 获取用户 {user_id} 文档列表")
    docs = list_user_documents(user_id)

    return [
        {
            "id": d.doc_id,
            "name": d.doc_name,
            "size": d.file_size,
            "time": str(d.upload_time)
        }
        for d in docs
    ]


def delete_user_document(doc_id: int, user_id: int):
    logger.debug(f"[Service] 删除用户 {user_id} 的文档 {doc_id}")
    is_deleted = delete_document(doc_id, user_id)

    if not is_deleted:
        raise ValueError("文档不存在或无权限删除")
    return is_deleted