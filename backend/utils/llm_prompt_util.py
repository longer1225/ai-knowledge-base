# backend/utils/llm_prompt_util.py
from backend.utils.llm_util import get_llm  # 调用你现成的单例
from backend.config.backend_base_settings import ENV_MODE
from backend.utils.logger import logger

def generate_chat_title(user_question: str) -> str:
    """
    根据用户第一条消息，生成 4~8 字聊天窗口标题
    完全复用你现有的 LLM 单例
    """
    try:
        # 开发环境直接返回简单标题，不调用模型
        if ENV_MODE == "dev":
            return "AI 智能问答"

        # 获取你已有的单例 LLM
        llm = get_llm()

        # 标题生成提示词
        prompt = f"""
请用4-8个字总结用户的问题，作为聊天标题。
只返回标题，不要任何多余内容、符号、解释。

问题：{user_question}
""".strip()

        # 调用模型
        title = llm.predict(prompt).strip()

        # 安全处理长度
        if len(title) > 8:
            title = title[:8]
        if len(title) < 2:
            return "智能对话"

        return title

    except Exception as e:
        logger.error(f"生成对话标题失败：{str(e)}")
        return "新对话"