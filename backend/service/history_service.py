# backend/service/history_service.py
# 只处理业务逻辑，调用Mapper层，完全不操作数据库会话
from ..mapper.history_mapper import get_history_by_user_id, insert_history, delete_history_by_user_id

# 获取用户QA历史（纯业务转发，无额外逻辑）
def get_user_qa_history(user_id: int):
    # 只调用Mapper，不碰db
    return get_history_by_user_id(user_id)

# 保存QA历史（可扩展业务逻辑，比如参数校验）
def save_qa_history(user_id: int, question: str, answer: str, source_chunks="", similarity_scores=""):
    # 业务校验：问题/回答不能为空
    if not question.strip() or not answer.strip():
        raise ValueError("问题和回答不能为空")
    # 调用Mapper执行插入
    return insert_history(user_id, question, answer, source_chunks, similarity_scores)

# 清空QA历史（纯业务转发）
def clear_user_qa_history(user_id: int):
    delete_history_by_user_id(user_id)