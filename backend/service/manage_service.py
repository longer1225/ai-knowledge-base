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

# 删除文档
def delete_user_document(doc_id: int, user_id: int):
    return delete_document(doc_id, user_id)