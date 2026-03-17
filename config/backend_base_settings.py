# config/base.py
# ===================== 基础通用配置（所有环境都用） =====================

ENV_MODE = "dev"
# 后端运行基础配置
BACKEND_CONFIG = {
    "host": "0.0.0.0",
    "port": 8001,
    "reload": True
}

# API基础地址
API_BASE_URL = f"http://127.0.0.1:{BACKEND_CONFIG['port']}"

# 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "postgres123",
    "database": "ai_knowledge_base",
}

# 文本切片配置
TEXT_SPLIT_CONFIG = {
    "chunk_size": 500,
    "chunk_overlap": 50
}

# JWT配置
SECRET_KEY = "1234567890abcdefghijklmnopqrstuvwxyz"
ALGORITHM = "HS256"

# 嵌入模型基础配置（只留通用字段，环境特有字段在dev/prod里加）
EMBEDDING_CONFIG = {
    "dimension": 384,  # 通用维度
    "api_key": "",     # 通用默认值
}

# config/backend_base_settings.py
# 原有配置不变，新增历史记录配置
HISTORY_CONFIG = {
    "keep_test_data": True,  # 通用默认值，开发/生产再覆盖
    "test_user_id": 0        # 测试用户ID（生产环境过滤该用户的记录）
}