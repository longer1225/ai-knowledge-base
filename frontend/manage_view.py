import streamlit as st
from utils.request_util import req_get, req_delete

def load_documents():
    try:
        data = req_get("/api/manage")  # 👈 直接用，不用 res.text

        if data.get("code") == 0:
            st.session_state.docs = data.get("data", [])
        else:
            st.session_state.docs = []
    except Exception as e:
        print("解析错误：", e)
        st.session_state.docs = []

def render():
    load_documents()
    st.markdown("<h2 style='color: white;'>📖 知识库管理</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.docs:
        for doc in st.session_state.docs:
            st.markdown(f"""
                <div class="dark-card">
                    <div>
                        <h4 style='margin:0; color:#ECECEC;'>📄 {doc['name']}</h4>
                        <p style='margin:5px 0 0 0; color:#888; font-size:14px;'>
                            大小: {doc['size']} B &nbsp;|&nbsp; 上传时间: {doc['time']}
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if st.button("🗑️ 删除", key=f"del_{doc['id']}"):
                req_delete(f"/api/manage/{doc['id']}")
                st.rerun()
    else:
        st.info("当前知识库为空，请前往「文档上传」页面添加文档。")