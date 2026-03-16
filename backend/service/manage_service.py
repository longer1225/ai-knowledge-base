from backend.mapper.document_mapper import list_user_documents, delete_document

# 获取文档列表
def get_user_documents(user_id: int):
    docs = list_user_documents(user_id)
    return [
        {
            "id": d.doc_id,
            "name": d.doc_name,
            "size": d.file_size,
            # 原来的错误：d.created_at → 改成 d.upload_time
            "time": str(d.upload_time)
        }
        for d in docs
    ]

# manage_service.py 优化后
def delete_user_document(doc_id: int, user_id: int):
    # 接收Mapper的返回值，判断是否删除成功
    is_deleted = delete_document(doc_id, user_id)
    if not is_deleted:
        raise ValueError("文档不存在或无权限删除")
    return is_deleted