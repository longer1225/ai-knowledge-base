import streamlit as st
import utils.api_client
from datetime import datetime

def render():
    st.markdown("<h2 style='color: white; margin-bottom: 20px;'>📤 文档上传</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #aaa;'>支持 docx / txt 格式，单次限传1个（≤10MB）</p>", unsafe_allow_html=True)

    file = st.file_uploader("选择文件", type=["docx", "txt"], label_visibility="collapsed")
"""

    if file:
        if st.button("开始上传与处理", type="primary"):
            with st.spinner("上传并处理文档中，请稍候..."):
                files = {"file": (file.name, file, file.type)}
                res = request_api("/api/upload", "POST", files=files)
                if res and res.get("code") == 0:
                    st.session_state.docs.append({
                        "id": res["data"]["doc_id"],
                        "name": file.name,
                        "size": file.size,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.success(f"✅ {file.name} 上传成功！")
                elif res:
                    st.error(res["msg"])
                    
"""