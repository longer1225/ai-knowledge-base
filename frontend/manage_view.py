import streamlit as st
from frontend.request_util import req_get

# 加载数据
def load_documents():
    try:  # 👈 只加这一行
        res = req_get("/api/manage")

        # ===================== 调试
        print("后端返回的原始数据：", res.text)
        data = res.json()
        print("解析后的数据：", data)
        # =====================

        if data.get("code") == 0:
            st.session_state.docs = data.get("data", [])
        else:
            st.session_state.docs = []
    except Exception as e:  # 👈 只加这一行
        print("解析错误：", e)  # 👈 只加这一行
        st.session_state.docs = []  # 👈 只加这一行

def render():
    # 强制每次刷新都加载数据
    load_documents()

    # -------------- 只保留标题，删掉会崩溃的按钮 --------------
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
                from frontend.request_util import req_delete
                req_delete(f"/api/manage/{doc['id']}")
                st.rerun()
    else:
        st.info("当前知识库为空，请前往「文档上传」页面添加文档。")