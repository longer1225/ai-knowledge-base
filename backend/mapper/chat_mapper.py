from backend.models.chat import Chat
from backend.models.qa_history import QAHistory
from backend.utils.db_util import db_connection
from backend.utils.orm_to_dict_util import to_dict
from backend.utils.logger import logger
from datetime import datetime


def format_time(dt: datetime | None) -> str | None:
    """统一时间格式化工具（兼容 datetime / str）"""
    if not dt:
        return None

    # ✅ 如果已经是字符串（你现在的情况）
    if isinstance(dt, str):
        return dt

    # ✅ 如果是 datetime
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    # ✅ 兜底（防御性）
    return str(dt)


# 创建新对话
@db_connection
def create_chat(user_id: int, title: str = "新对话", db=None):
    chat = Chat(user_id=user_id, title=title)
    db.add(chat)
    db.flush()
    db.refresh(chat)

    chat_dict = to_dict(chat)
    chat_dict["create_time"] = format_time(chat_dict.get("create_time"))
    return chat_dict


# 查询用户的所有对话
@db_connection
def get_user_chats(user_id: int, db=None):
    chats = db.query(Chat) \
        .filter(Chat.user_id == user_id) \
        .order_by(Chat.create_time.desc()) \
        .all()

    chat_list = to_dict(chats)

    for item in chat_list:
        item["create_time"] = format_time(item.get("create_time"))

    return chat_list


# 获取单个对话
@db_connection
def get_chat_by_id(chat_id: int, user_id: int, db=None):
    chat = db.query(Chat) \
        .filter(Chat.chat_id == chat_id, Chat.user_id == user_id) \
        .first()

    if not chat:
        return None

    chat_dict = to_dict(chat)
    chat_dict["create_time"] = format_time(chat_dict.get("create_time"))
    return chat_dict


# 删除对话
@db_connection
def delete_chat_by_id(chat_id: int, user_id: int, db=None):
    chat = db.query(Chat).filter(
        Chat.chat_id == chat_id,
        Chat.user_id == user_id
    ).first()

    if chat:
        db.delete(chat)
        db.commit()
        return True

    return False


# 删除对话关联的历史记录
@db_connection
def delete_qa_history_by_chat(chat_id: int, user_id: int, db=None):
    db.query(QAHistory) \
        .filter(
            QAHistory.chat_id == chat_id,
            QAHistory.user_id == user_id
        ) \
        .delete(synchronize_session=False)

    db.commit()
    return True


# 更新对话标题
@db_connection
def update_chat_title(chat_id: int, user_id: int, new_title: str, db=None):
    chat = db.query(Chat).filter(
        Chat.chat_id == chat_id,
        Chat.user_id == user_id
    ).first()

    if chat:
        chat.title = new_title
        db.commit()

        chat_dict = to_dict(chat)
        chat_dict["create_time"] = format_time(chat_dict.get("create_time"))
        return chat_dict

    return None