import streamlit as st

from backend.config import ENV_MODE
from backend.utils.logger import logger
from frontend.request_util import req_post, req_get, req_stream_post

# ==================== 全局初始化 ====================
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

# ==================== API 函数 ====================
def create_chat():
    try:
        logger.info("[前端] 调用新建对话接口")
        res = req_post("/api/chat/new", {})
        if res and res.get("code") == 0:
            return res["data"]["chat_id"]
    except Exception as e:
        logger.error(f"[前端] 新建对话失败：{e}")
        st.error("新建对话出错啦～")
    return None


# 🔥 ✅ 修复版：自动从全局获取 chat_id，不用传参！
def qa_ask(question):
    try:
        # 🔥 全局获取当前对话 ID（企业级标准写法）
        chat_id = st.session_state.get("chat_id")

        logger.info("=" * 50)
        logger.info(f"[前端QA] 用户问题：{question}")
        logger.info(f"[前端QA] 全局 chat_id = {chat_id}")

        # ✅ 自动带上 chat_id，不用到处传参
        return req_stream_post("/api/qa/ask", {
            "question": question,
            "chat_id": chat_id
        })

    except Exception as e:
        logger.error(f"[前端QA] 请求异常：{str(e)}")
        return "⚠️ 网络异常或服务未启动"


def load_chat_history(chat_id):
    try:
        logger.info(f"[前端] 加载聊天记录：{chat_id}")
        res = req_get(f"/api/history/chat/{chat_id}")
        if res and res.get("code") == 0:
            return res["data"]
    except Exception as e:
        logger.error(f"[前端] 加载历史失败：{e}")
    return []


def save_chat_msg(question, answer, chat_id):
    try:
        logger.info("[前端] 保存消息到历史")
        req_post("/api/history/qa", {
            "question": question,
            "answer": answer,
            "chat_id": chat_id
        })
        logger.info(f"[前端✅] 消息保存成功 chat_id={chat_id}")
    except Exception as e:
        logger.error(f"[前端] 保存消息失败：{e}")


# ==================== 主渲染函数 ====================
def render():
    if not st.session_state.get("token"):
        st.error("❌ 请先登录再使用问答功能")
        return

    current_chat_id = st.session_state.chat_id
    logger.info(f"[render] 当前 chat_id = {current_chat_id}")

    st.title("💬 AI 知识库问答")

    if not current_chat_id:
        st.info("👈 点击左侧「新聊天」开始对话")
        return

    # 显示消息
    chat_history = load_chat_history(current_chat_id)
    for msg in reversed(chat_history):
        with st.chat_message("user"):
            st.markdown(msg["question"])
        with st.chat_message("assistant"):
            st.markdown(msg["answer"])

    # 输入框
    question = st.chat_input("输入你的问题...")
    if question and question.strip():
        logger.info(f"[前端✅] 用户发送消息：{question} | chat_id={current_chat_id}")

        with st.chat_message("user"):
            st.markdown(question)

        with st.spinner("🤖 思考中..."):
            # ✅ 干净！不用传 chat_id！
            answer = qa_ask(question)

        with st.chat_message("assistant"):
            st.markdown(answer)

        save_chat_msg(question, answer, current_chat_id)

        logger.info(f"[前端✅] 准备刷新页面 chat_id={current_chat_id}")

        # ✅ 新版 streamlit 标准写法
        st.rerun()