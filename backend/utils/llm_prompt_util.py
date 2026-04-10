# backend/utils/llm_prompt_util.py

from backend.utils.llm_util import get_llm
from backend.config.backend_base_settings import ENV_MODE
from backend.utils.logger import logger


def generate_chat_title(user_question: str) -> str:
    """
    根据用户第一条消息，生成 4~8 字聊天窗口标题
    """
    try:
        # 开发环境直接返回
        if ENV_MODE == "dev":
            return "AI问答"

        llm = get_llm()

        prompt = f"""
请用4-8个字总结用户的问题，作为聊天标题。

要求：
1. 只返回标题
2. 不要标点符号
3. 不要解释
4. 不超过8个字

问题：{user_question}
""".strip()

        # ✅ 用你自己的统一接口
        title = llm.generate(prompt).strip()

        # ======================
        # 安全处理（非常重要）
        # ======================

        # 去掉奇怪符号
        title = title.replace("\n", "").replace(" ", "")

        # 长度限制
        if len(title) > 8:
            title = title[:8]

        if len(title) < 2:
            return "智能对话"

        return title

    except Exception as e:
        logger.error(f"生成对话标题失败：{str(e)}")
        return "新对话"