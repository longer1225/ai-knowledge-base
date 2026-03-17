import streamlit as st
from utils.request_util import req_post, req_get, req_delete
from utils.logger import logger

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

def qa_ask(question):
    try:
        res = req_post("/api/qa/ask", {"question": question})
        if res and res.get("code") == 0:
            return res["data"]["answer"]
    except Exception as e:
        logger.error(f"问答请求失败：{e}")
    return "抱歉，我没理解你的问题～"

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

# ==================== 主渲染函数（只保留聊天区域） ====================
def render():
    # 登录校验
    if not st.session_state.get("token"):
        st.error("❌ 请先登录再使用哦！")
        return

    st.title("💬 AI 知识库问答")

    # ==================== 主聊天区域 ====================
    current_chat_id = st.session_state.chat_id
    if not current_chat_id:
        st.info("👈 点击左侧「新聊天」，开始你的问答吧！")
        return

    # 显示历史消息
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