from backend.models import Chat, QAHistory
from utils.db_util import db_connection
from utils.logger import logger


# 创建新对话
@db_connection
def create_chat(user_id: int, title: str = "新对话", db=None):
    chat = Chat(user_id=user_id, title=title)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


# 查询用户的所有对话
@db_connection
def get_user_chats(user_id: int, db=None):
    return db.query(Chat).filter(Chat.user_id == user_id).order_by(Chat.create_time.desc()).all()


# 获取单个对话
@db_connection
def get_chat_by_id(chat_id: int, user_id: int, db=None):
    return db.query(Chat).filter(Chat.chat_id == chat_id, Chat.user_id == user_id).first()

# 删除对话
@db_connection
def delete_chat_by_id(chat_id: int, user_id: int, db=None):
    chat = db.query(Chat).filter(Chat.chat_id == chat_id, Chat.user_id == user_id).first()
    if chat:
        db.delete(chat)
        db.commit()
        return True
    return False

# 删除对话关联的历史记录
@db_connection
def delete_qa_history_by_chat(chat_id: int, user_id: int, db=None):
    db.query(QAHistory).filter(QAHistory.chat_id == chat_id, QAHistory.user_id == user_id).delete()
    db.commit()
    return True

@db_connection
def update_chat_title(chat_id: int, user_id: int, new_title: str, db=None):
    chat = db.query(Chat).filter(Chat.chat_id == chat_id, Chat.user_id == user_id).first()
    if chat:
        chat.title = new_title
        db.commit()