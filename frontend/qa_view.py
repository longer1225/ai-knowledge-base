import streamlit as st
# 在 qa_view.py 顶部导入
from frontend.request_util import req_post, req_get

# 调用后端问答接口（自动带 token）
def ask_question(question):
    res = req_post("/api/qa/ask", data={"question": question})
    return res.json()

# 调用后端获取历史接口（自动带 token）
def get_history():
    res = req_get("/api/history/list")
    return res.json()

# 自动带 token 请求
def qa_chat(token, question):
    return req_post("/api/qa/ask", {
        "question": question
    }).json()

def render():
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []

    if not st.session_state.qa_history:
        st.markdown('<div class="welcome-title">有什么可以帮忙的？</div>', unsafe_allow_html=True)
    else:
        for item in st.session_state.qa_history:
            with st.chat_message("user", avatar="🧑‍💻"):
                st.write(item["question"])
            with st.chat_message("assistant", avatar="🤖"):
                st.write(item["answer"])
                if item.get("source"):
                    with st.expander("🔍 参考来源", expanded=False):
                        st.write(item["source"])

    prompt = st.chat_input("有问题，尽管问...")
    if prompt:
        st.session_state.qa_history.append({"question": prompt, "answer": "", "source": ""})
        st.rerun()

    if st.session_state.qa_history and st.session_state.qa_history[-1]["answer"] == "":
        question = st.session_state.qa_history[-1]["question"]
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("思考中..."):
                res = qa_chat(st.session_state.get("token"), question)
                if res and res.get("code") == 0:
                    st.session_state.qa_history[-1]["answer"] = res["answer"]
                    st.session_state.qa_history[-1]["source"] = res.get("source", "")
                else:
                    st.error("请求失败")
                    st.session_state.qa_history.pop()
        st.rerun()
