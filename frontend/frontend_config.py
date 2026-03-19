# frontend_config.py（在原有基础上新增/修改）
import streamlit as st

def init_session_state():
    """初始化Session State（补充登录相关字段）"""
    # 保留你原有初始化逻辑，新增登录字段
    if "docs" not in st.session_state:
        st.session_state.docs = []
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []
    if "current_page" not in st.session_state:
        st.session_state.current_page = "智能问答"
    # 新增登录相关
    if "login_user" not in st.session_state:
        st.session_state.login_user = None
    if "token" not in st.session_state:
        st.session_state.token = None

def load_css():
    """加载CSS（保留你的原有样式，新增登录表单样式）"""
    st.markdown("""
        <style>
        
        /* 修复 Primary 主要按钮（登录/注册按钮）白底白字的问题，强制让里面的字变成黑色 */
    button[kind="primary"] {
        background-color: #FFFFFF !important;
        border: 1px solid #FFFFFF !important;
    }
    button[kind="primary"] * {
        color: #000000 !important; 
        font-weight: bold !important;
    }
    /* 你的原有CSS（完全保留） */
    .stApp, .main {
        background-color: #212121 !important;
        color: #ECECEC !important;
    }
    [data-testid="stSidebar"] {
        background-color: #171717 !important;
        border-right: none !important;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stSidebarNav"] {display: none;} 

    .sidebar-btn-container button {
        width: 100%;
        background-color: transparent !important;
        border: 1px solid transparent !important;
        color: #ECECEC !important;
        text-align: left !important;
        padding: 10px 15px !important;
        border-radius: 8px !important;
        font-size: 14px !important;
        transition: all 0.2s;
    }
    .sidebar-btn-container button p {
        color: #ECECEC !important; 
    }
    [data-testid="stSidebar"] .sidebar-btn-container button:hover,
    [data-testid="stSidebar"] .sidebar-btn-container button:focus,
    [data-testid="stSidebar"] .sidebar-btn-container button:active {
        background-color: #2F2F2F !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
        box-shadow: none !important;
        outline: none !important;
    }
    [data-testid="stSidebar"] .sidebar-btn-container button:hover *,
    [data-testid="stSidebar"] .sidebar-btn-container button:focus *,
    [data-testid="stSidebar"] .sidebar-btn-container button:active * {
        color: #FFFFFF !important;
    }
    .welcome-title {
        color: #FFFFFF;
        font-size: 32px;
        font-weight: 500;
        text-align: center;
        margin-top: 25vh; 
        margin-bottom: 40px;
    }
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 1.5rem !important;
    }
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(255,255,255,0.02) !important; 
    }
    [data-testid="stChatInput"] {
        background-color: #2F2F2F !important;
        border: 1px solid #424242 !important;
        border-radius: 20px !important;
    }
    [data-testid="stChatInput"] textarea {
        color: white !important;
    }
    .dark-card {
        background-color: #2F2F2F;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #424242;
    }
    .stFileUploader > div > div {
        background-color: #2F2F2F !important;
        border: 1px dashed #555 !important;
    }

    /* 新增：GPT风格登录/注册表单样式 */
    .auth-container {
        max-width: 400px;
        margin: 10vh auto;
        padding: 30px;
        background-color: #2F2F2F;
        border-radius: 12px;
        border: 1px solid #424242;
    }
    .auth-title {
        text-align: center;
        font-size: 24px;
        font-weight: 500;
        margin-bottom: 25px;
        color: #FFFFFF;
    }
    .login-hint {
        text-align: center;
        padding: 20px;
        color: #FF9800;
        font-size: 18px;
        margin-top: 20vh;
    }
    </style>
    """, unsafe_allow_html=True)