from backend.models.qa_history import QAHistory
from backend.utils.db_util import db_connection
from backend.utils.orm_to_dict_util import to_dict
from backend.utils.logger import logger
from datetime import datetime


def format_time(dt):
    """统一时间格式化工具（兼容 datetime / str）"""
    if dt is None:
        return None

    if isinstance(dt, str):
        return dt  # 已经是字符串，直接返回

    return dt.strftime("%Y-%m-%d %H:%M:%S")


# 根据【窗口ID】查询历史
@db_connection
def get_history_by_chat_id(user_id: int, chat_id: int, db=None):
    logger.debug(f"[Mapper] 查询用户 {user_id} 窗口 {chat_id} 历史")
    history = db.query(QAHistory)\
        .filter(
            QAHistory.user_id == user_id,
            QAHistory.chat_id == chat_id
        )\
        .order_by(QAHistory.create_time.asc())\
        .all()

    # 自动转换 + 时间格式化
    hist_list = to_dict(history)
    for item in hist_list:
        item["create_time"] = format_time(item["create_time"])
    return hist_list


# 查用户全部历史
@db_connection
def get_history_by_user_id(user_id: int, db=None):
    logger.debug(f"[Mapper] 查询用户 {user_id} QA历史")
    history = db.query(QAHistory)\
        .filter(QAHistory.user_id == user_id)\
        .order_by(QAHistory.create_time.desc())\
        .all()

    hist_list = to_dict(history)
    for item in hist_list:
        item["create_time"] = format_time(item["create_time"])
    return hist_list


# 插入历史 → 返回完整字典（标准化）
@db_connection
def insert_history(
    user_id: int,
    question: str,
    answer: str,
    source_chunks: str = "",
    similarity_scores: str = "",
    chat_id: int = None,
    db=None
):
    logger.debug(f"[Mapper] 插入历史，用户：{user_id}，窗口：{chat_id}")
    new_history = QAHistory(
        user_id=user_id,
        question=question,
        answer=answer,
        source_chunks=source_chunks,
        similarity_scores=similarity_scores,
        chat_id=chat_id
    )
    db.add(new_history)
    db.flush()
    db.refresh(new_history)

    # 自动转换 + 时间格式化
    hist_dict = to_dict(new_history)
    hist_dict["create_time"] = format_time(hist_dict["create_time"])
    return hist_dict


# 删除用户历史
@db_connection
def delete_history_by_user_id(user_id: int, db=None):
    logger.debug(f"[Mapper] 删除用户 {user_id} 全部QA历史")
    count = db.query(QAHistory).filter(QAHistory.user_id == user_id).delete()
    db.commit()
    return count  # 返回删除条数，保持不变