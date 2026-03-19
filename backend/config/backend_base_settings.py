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
# 嵌入模型基础配置
EMBEDDING_CONFIG = {
    "model_type": "",      # mock / online
    "model_name": "",
    "dimension": 384,
    "api_key": "",
    "base_url": ""
}

# LLM 大模型基础配置
LLM_CONFIG = {
    "model_type": "",      # mock / ollama / zhipu / qwen
    "model_name": "",
    "temperature": 0.1,
    "max_tokens": 2048,
    "api_key": "",
    "base_url": ""
}

TOP_K = 3  # 最佳匹配条数，以后这里改就行

# 历史记录配置
HISTORY_CONFIG = {
    "keep_test_data": True,
    "test_user_id": 0
}