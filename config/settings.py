# settings.py
# ===================== 全局环境配置 =====================
# dev  = 开发模式（不调用LLM，不花钱，适合调试）
# prod = 生产模式（正式运行，调用LLM）
ENV_MODE = "dev"  # 只需改这里，全局生效

# ===================== 后端运行配置 =====================
BACKEND_CONFIG = {
    "host": "0.0.0.0",
    "port": 8001,       # 后端运行端口
    "reload": True      # 开发模式开启热重载，生产模式改为False
}

# ===================== API基础地址（前端用） =====================
# 前端访问后端的地址，端口必须和BACKEND_CONFIG["port"]一致
API_BASE_URL = f"http://127.0.0.1:{BACKEND_CONFIG['port']}"

# ===================== 数据库配置 =====================
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "postgres123",
    "database": "ai_knowledge_base",
}

# ===================== 文本切片配置 =====================
TEXT_SPLIT_CONFIG = {
    "chunk_size": 500,
    "chunk_overlap": 50
}

# ===================== JWT配置 =====================
SECRET_KEY = "1234567890abcdefghijklmnopqrstuvwxyz"
ALGORITHM = "HS256"

# ===================== 嵌入模型配置 =====================
EMBEDDING_CONFIG = {
    "model_type": "mock",    # 切换模型只需改这一行
    "dimension": 384,
    # "api_key": "xxx",        # 未来对接在线模型时使用
}