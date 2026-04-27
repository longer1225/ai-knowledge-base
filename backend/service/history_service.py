from ..core.exceptions import ParamException
from ..mapper.history_mapper import (
    get_history_by_user_id,
    get_history_by_chat_id,
    insert_history,
    delete_history_by_user_id
)
from ..utils.logger import logger
from ..utils.log_util import insert_operation_log  # 加这一行


# ==========================
# 获取用户全部历史
# ==========================
def get_user_qa_history(user_id: int):
    logger.debug(f"[Service] 获取用户 {user_id} QA历史")

    # Mapper 已经返回 list[dict]，直接用
    records = get_history_by_user_id(user_id)

    # 统一返回格式（字段对齐 mapper）
    return [
        {
            "qa_id": r["qa_id"],
            "question": r["question"],
            "answer": r["answer"],
            "source_chunks": r["source_chunks"],
            "similarity_scores": r["similarity_scores"],
            "chat_id": r["chat_id"],
            "create_time": r["create_time"]  # mapper 已格式化，无需处理
        }
        for r in records
    ]


# ==========================
# 按聊天窗口查询
# ==========================
def get_qa_history_by_chat(user_id: int, chat_id: int):
    logger.debug(f"[Service] 获取用户 {user_id} 窗口 {chat_id} 历史记录")

    records = get_history_by_chat_id(user_id, chat_id)

    return [
        {
            "qa_id": r["qa_id"],
            "question": r["question"],
            "answer": r["answer"],
            "source_chunks": r["source_chunks"],
            "similarity_scores": r["similarity_scores"],
            "chat_id": r["chat_id"],
            "create_time": r["create_time"]
        }
        for r in records
    ]


# ==========================
# 保存 QA
# ==========================
def save_qa_history(
    user_id: int,
    question: str,
    answer: str,
    source_chunks="",
    similarity_scores="",
    chat_id: int = None
):
    logger.debug(f"[Service] 保存用户 {user_id} QA历史，窗口：{chat_id}")

    if not question or not question.strip():
        raise ParamException("问题不能为空")

    if not answer or not answer.strip():
        raise ParamException("回答不能为空")

    # mapper 返回字典，直接返回统一格式
    history = insert_history(
        user_id=user_id,
        question=question,
        answer=answer,
        source_chunks=source_chunks,
        similarity_scores=similarity_scores,
        chat_id=chat_id
    )

    # 统一返回（和列表接口字段一致）
    return {
        "qa_id": history["qa_id"],
        "question": history["question"],
        "answer": history["answer"],
        "source_chunks": history["source_chunks"],
        "similarity_scores": history["similarity_scores"],
        "chat_id": history["chat_id"],
        "create_time": history["create_time"]
    }


# ==========================
# 清空历史
# ==========================
def clear_user_qa_history(user_id: int):
    logger.debug(f"[Service] 清空用户 {user_id} QA历史")
    delete_history_by_user_id(user_id)
    # ======================
    # 清空历史日志
    # ======================
    insert_operation_log(
        user_id=user_id,
        operation="清空历史",
        module="问答历史",
        content="用户清空了全部问答记录"
    )

    return True