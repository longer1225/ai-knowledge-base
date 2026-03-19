import streamlit as st

from backend.config import ENV_MODE
from backend.utils.logger import logger
# 🔥 导入流式方法
from frontend.request_util import req_post, req_get, req_stream_post

# ==================== 全局初始化 ====================
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

# ==================== API 函数 ====================
def create_chat():
    try:
        res = req_post("/api/chat/new", {})
        if res and res.get("code") == 0:
            return res["data"]["chat_id"]
    except Exception as e:
        logger.error(f"新建对话失败：{e}")
        st.error("新建对话出错啦～")
    return None


# ==============================
# 🔥 分模式：DEV JSON / PROD 流式
# ==============================
def qa_ask(question):
    try:
        # --------------------------
        # ✅ DEV 模式：JSON
        # --------------------------
        if ENV_MODE == "dev":
            res = req_post("/api/qa/ask", {"question": question})

            if res is None:
                return "⚠️ 服务未响应，请检查后端是否启动"

            if res.get("code") == 0:
                return res["data"]["answer"]
            else:
                return res.get("msg", "服务异常，请稍后重试")

        # --------------------------
        # ✅ PROD 模式：流式（走工具类，不绕过！）
        # --------------------------
        else:
            return req_stream_post("/api/qa/ask", {"question": question})

    except Exception as e:
        logger.error(f"问答请求失败：{e}")
        return "⚠️ 网络异常或服务未启动"


def load_chat_history(chat_id):
    try:
        res = req_get(f"/api/history/chat/{chat_id}")
        if res and res.get("code") == 0:
            return res["data"]
    except Exception as e:
        logger.error(f"加载历史失败：{e}")
    return []


def save_chat_msg(question, answer, chat_id):
    try:
        req_post("/api/history/qa", {
            "question": question,
            "answer": answer,
            "chat_id": chat_id
        })
    except Exception as e:
        logger.error(f"保存消息失败：{e}")


# ==================== 主渲染函数 ====================
def render():
    if not st.session_state.get("token"):
        st.error("❌ 请先登录再使用问答功能")
        return

    st.title("💬 AI 知识库问答")

    current_chat_id = st.session_state.chat_id
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
        with st.chat_message("user"):
            st.markdown(question)

        with st.spinner("🤖 思考中..."):
            answer = qa_ask(question)

        with st.chat_message("assistant"):
            st.markdown(answer)

        save_chat_msg(question, answer, current_chat_id)
        st.rerun()