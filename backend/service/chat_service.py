from backend.mapper.chat_mapper import create_chat, get_user_chats, get_chat_by_id, delete_chat_by_id, \
    delete_qa_history_by_chat

from backend.mapper.chat_mapper import update_chat_title

def update_chat_title_service(chat_id: int, user_id: int, new_title: str):
    return update_chat_title(chat_id, user_id, new_title)
# 新建对话
def create_new_chat(user_id: int):
    return create_chat(user_id=user_id)


# 获取对话列表
def list_user_chats(user_id: int):
    return get_user_chats(user_id=user_id)


# 获取对话详情
def get_chat(chat_id: int, user_id: int):
    return get_chat_by_id(chat_id=chat_id, user_id=user_id)

# 删除对话
def delete_chat(chat_id: int, user_id: int):
    return delete_chat_by_id(chat_id, user_id)

# 删除对话关联的历史
def delete_qa_by_chat(chat_id: int, user_id: int):
    return delete_qa_history_by_chat(chat_id, user_id)