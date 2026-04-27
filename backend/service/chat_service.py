from backend.mapper.chat_mapper import (
    create_chat,
    get_user_chats,
    get_chat_by_id,
    delete_chat_by_id,
    delete_qa_history_by_chat,
    update_chat_title
)
from backend.utils.redis_cache import redis_cache
import json
from backend.utils.log_util import insert_operation_log  # 加这一行

# ==========================
# 🔥 重要：因为 Mapper 已经返回字典，不再需要 chat_to_dict 工具函数！
# ==========================

# ==========================
# 更新标题
# ==========================
def update_chat_title_service(chat_id: int, user_id: int, new_title: str):
    res = update_chat_title(chat_id, user_id, new_title)

    # 清缓存
    redis_cache.delete(f"user:chats:{user_id}")
    redis_cache.delete(f"chat:info:{chat_id}")
    # 🔥 修改标题日志
    insert_operation_log(
        user_id=user_id,
        operation="修改标题",
        module="对话管理",
        content=f"对话 {chat_id} 修改标题为：{new_title}"
    )

    return res


# ==========================
# 新建对话
# ==========================
def create_new_chat(user_id: int):
    # 🔥 Mapper 已经直接返回 dict，不需要 chat_to_dict
    chat = create_chat(user_id=user_id)

    redis_cache.delete(f"user:chats:{user_id}")

    # 🔥 新建对话日志
    insert_operation_log(
        user_id=user_id,
        operation="新建对话",
        module="对话管理",
        content=f"创建对话窗口：{chat['chat_id']}"
    )

    return chat  # 直接返回字典


# ==========================
# 获取对话列表（统一返回 dict）
# ==========================
def list_user_chats(user_id: int):
    cache_key = f"user:chats:{user_id}"
    cache_data = redis_cache.get(cache_key)

    if cache_data:
        return json.loads(cache_data)

    # 🔥 Mapper 已经返回 list[dict]
    chats = get_user_chats(user_id=user_id)

    # 🔥 不需要再转换！直接用
    redis_cache.set(
        cache_key,
        json.dumps(chats, ensure_ascii=False),
        ex=600
    )

    return chats


# ==========================
# 获取单个对话
# ==========================
def get_chat(chat_id: int, user_id: int):
    cache_key = f"chat:info:{chat_id}"
    cache_data = redis_cache.get(cache_key)

    if cache_data:
        return json.loads(cache_data)

    # 🔥 Mapper 已经返回 dict / None
    chat = get_chat_by_id(chat_id=chat_id, user_id=user_id)

    if chat:
        redis_cache.set(
            cache_key,
            json.dumps(chat, ensure_ascii=False),
            ex=600
        )
        return chat

    return None


# ==========================
# 删除对话
# ==========================
def delete_chat(chat_id: int, user_id: int):
    res = delete_chat_by_id(chat_id, user_id)

    redis_cache.delete(f"user:chats:{user_id}")
    redis_cache.delete(f"chat:info:{chat_id}")
    redis_cache.delete(f"chat:history:{chat_id}")

    # 🔥 删除对话日志
    insert_operation_log(
        user_id=user_id,
        operation="删除对话",
        module="对话管理",
        content=f"删除对话窗口：{chat_id}"
    )

    return res


# ==========================
# 删除QA历史
# ==========================
def delete_qa_by_chat(chat_id: int, user_id: int):
    res = delete_qa_history_by_chat(chat_id, user_id)

    redis_cache.delete(f"chat:history:{chat_id}")

    # 🔥 删除单窗口历史日志
    insert_operation_log(
        user_id=user_id,
        operation="清空对话记录",
        module="对话管理",
        content=f"清空对话 {chat_id} 下的问答记录"
    )

    return res