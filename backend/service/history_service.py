from ..mapper.history_mapper import get_history_by_user_id, insert_history, delete_history_by_user_id
from backend.exceptions import ParamException
from utils.logger import logger


def get_user_qa_history(user_id: int):
    logger.debug(f"[Service] 获取用户 {user_id} QA历史")
    return get_history_by_user_id(user_id)


def save_qa_history(user_id: int, question: str, answer: str, source_chunks="", similarity_scores=""):
    logger.debug(f"[Service] 保存用户 {user_id} QA历史")

    if not question or not question.strip():
        raise ParamException("问题不能为空")
    if not answer or not answer.strip():
        raise ParamException("回答不能为空")

    return insert_history(user_id, question, answer, source_chunks, similarity_scores)


def clear_user_qa_history(user_id: int):
    logger.debug(f"[Service] 清空用户 {user_id} QA历史")
    delete_history_by_user_id(user_id)