from backend.models.document_chunk import DocumentChunk
from backend.models.qa_history import QAHistory
from backend.utils.db_util import db_connection
from backend.utils.orm_to_dict_util import to_dict
from backend.utils.logger import logger
from datetime import datetime


def format_time(dt: datetime | None) -> str | None:
    """统一时间格式化工具（兼容 datetime / str）"""
    if not dt:
        return None

    # ✅ 已经是字符串
    if isinstance(dt, str):
        return dt

    # ✅ datetime → 格式化
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    # ✅ 兜底
    return str(dt)


# ====================== 【原有必备功能】全部保留 ======================
@db_connection
def list_all_document_chunks(db=None):
    logger.debug("[Mapper] 查询所有文档切片")
    chunks = db.query(DocumentChunk).all()

    return to_dict(chunks)


@db_connection
def insert_qa_history(
    user_id: int,
    question: str,
    answer: str,
    source_chunks: str = "",
    similarity_scores: str = "",
    chat_id: int = None,
    db=None
):
    logger.debug(f"[Mapper] 插入QA历史，用户：{user_id}，窗口：{chat_id}")

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

    hist_dict = to_dict(new_history)
    hist_dict["create_time"] = format_time(hist_dict.get("create_time"))

    return hist_dict


# ====================== 多窗口：按窗口查询历史 ======================
@db_connection
def get_history_by_chat_id(user_id: int, chat_id: int, db=None):
    logger.debug(f"[Mapper] 查询用户 {user_id} 窗口 {chat_id} 历史")

    history = db.query(QAHistory) \
        .filter(
            QAHistory.user_id == user_id,
            QAHistory.chat_id == chat_id
        ) \
        .order_by(QAHistory.create_time.desc()) \
        .all()

    hist_list = to_dict(history)

    for item in hist_list:
        item["create_time"] = format_time(item.get("create_time"))

    return hist_list


# ====================== 原有：查询用户全部历史 ======================
@db_connection
def get_history_by_user_id(user_id: int, db=None):
    logger.debug(f"[Mapper] 查询用户 {user_id} QA历史")

    history = db.query(QAHistory) \
        .filter(QAHistory.user_id == user_id) \
        .order_by(QAHistory.create_time.desc()) \
        .all()

    hist_list = to_dict(history)

    for item in hist_list:
        item["create_time"] = format_time(item.get("create_time"))

    return hist_list


# ====================== 原有：删除用户历史 ======================
@db_connection
def delete_history_by_user_id(user_id: int, db=None):
    logger.debug(f"[Mapper] 删除用户 {user_id} 全部QA历史")

    count = db.query(QAHistory) \
        .filter(QAHistory.user_id == user_id) \
        .delete()

    db.commit()

    return count