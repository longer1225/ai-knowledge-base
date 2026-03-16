import streamlit as st
from frontend.request_util import req_post, req_get

# 调用QA问答接口
def qa_chat(question):
    """调用后端QA接口，返回回答"""
    try:
        res = req_post("/api/qa/ask", {"question": question})
        data = res.json()
        return data.get("data", {}).get("answer", "")
    except Exception as e:
        st.error(f"❌ 问答接口调用失败：{str(e)}")
        return ""

# 从后端加载当前用户的QA历史
def load_user_qa_history():
    """加载并返回当前用户的历史对话，无则返回空列表"""
    try:
        res = req_get("/api/history/qa")
        data = res.json()
        if data.get("code") == 0:
            return data.get("data", [])
        else:
            st.warning(f"⚠️ 加载历史失败：{data.get('msg', '未知错误')}")
            return []
    except Exception as e:
        st.warning(f"⚠️ 连接后端失败，无法加载历史：{str(e)}")
        return []

# 保存一条QA记录到后端
def save_user_qa_history(question, answer):
    """保存对话记录到数据库（绑定当前用户）"""
    try:
        req_post("/api/history/qa", {
            "question": question,
            "answer": answer
        })
    except Exception as e:
        st.warning(f"⚠️ 历史记录保存失败：{str(e)}")

def render():
    st.title("💬 AI 知识库问答")

    # 1. 验证登录（无token直接拦截）
    token = st.session_state.get("token")
    if not token:
        st.error("❌ 请先登录后再使用问答功能！")
        return

    # 2. 加载历史（每次渲染都从后端读，保证数据最新）
    qa_history = load_user_qa_history()

    # 3. 展示历史对话（从后端读取的真实数据，按时间正序展示）
    # 注意：后端返回的是倒序，这里反转成正序
    for chat in reversed(qa_history):
        with st.chat_message("user"):
            st.markdown(chat["question"])
        with st.chat_message("assistant"):
            st.markdown(chat["answer"])

    # 4. 提问输入框
    question = st.chat_input("请输入你的问题...")
    if question and question.strip():
        # 4.1 显示用户问题
        with st.chat_message("user"):
            st.markdown(question)

        # 4.2 调用QA接口获取回答
        with st.spinner("🤖 正在思考..."):
            answer = qa_chat(question)
            # 无回答时的提示
            final_answer = answer if answer else "⚠️ 模型未加载，请先加载大模型后再提问！"

        # 4.3 显示助手回答
        with st.chat_message("assistant"):
            st.markdown(final_answer)

        # 4.4 保存记录到后端（核心：绑定用户ID，永久存储）
        save_user_qa_history(question, final_answer)

        # 4.5 重新加载历史（刷新展示）
        st.rerun()