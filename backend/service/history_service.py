from ..core.exceptions import ParamException
from ..mapper.history_mapper import (
    get_history_by_user_id,
    get_history_by_chat_id,
    insert_history,
    delete_history_by_user_id
)
from ..utils.logger import logger


def get_user_qa_history(user_id: int):
    logger.debug(f"[Service] 获取用户 {user_id} QA历史")
    return get_history_by_user_id(user_id)


# 按窗口查询
def get_qa_history_by_chat(user_id: int, chat_id: int):
    logger.debug(f"[Service] 获取用户 {user_id} 窗口 {chat_id} 历史记录")
    return get_history_by_chat_id(user_id, chat_id)


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

    return insert_history(
        user_id, question, answer,
        source_chunks, similarity_scores,
        chat_id
    )


def clear_user_qa_history(user_id: int):
    logger.debug(f"[Service] 清空用户 {user_id} QA历史")
    delete_history_by_user_id(user_id)