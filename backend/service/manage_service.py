from backend.mapper.document_mapper import list_user_documents, delete_document
from backend.utils.logger import logger
from backend.utils.redis_cache import redis_cache
from backend.utils.log_util import insert_operation_log  # 加这里

# ==========================
# 获取用户文档列表
# ==========================
def get_user_documents(user_id: int):
    logger.debug(f"[Service] 获取用户 {user_id} 文档列表")

    docs = list_user_documents(user_id)

    return [
        {
            "id": d["doc_id"],
            "name": d["doc_name"],
            "size": d["file_size"],
            # 🔥 修复：mapper 里是 create_time，不是 upload_time
            "time": d.get("create_time")
        }
        for d in docs
    ]


# ==========================
# 删除文档（完整版）
# ==========================
def delete_user_document(doc_id: int, user_id: int):
    logger.debug(f"[Service] 删除用户 {user_id} 的文档 {doc_id}")

    is_deleted = delete_document(doc_id, user_id)

    if not is_deleted:
        raise ValueError("文档不存在或无权限删除")

    # 删除文档缓存
    doc_cache_key = f"rag:doc:{doc_id}:chunks"
    logger.info(f"[Redis] 删除缓存: {doc_cache_key}")
    redis_cache.delete(doc_cache_key)

    # 更新版本号，让缓存失效
    logger.info("[Redis] 更新 RAG 版本号（缓存失效）")
    redis_cache.incr("rag:version")

    # 清理全局缓存
    redis_cache.delete("rag:all_chunks")
    # ======================
    # 文档删除日志
    # ======================
    insert_operation_log(
        user_id=user_id,
        operation="文档删除",
        module="文档知识库",
        content=f"删除文档ID：{doc_id}"
    )

    return is_deleted