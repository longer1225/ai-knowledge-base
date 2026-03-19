import os

# ===================== 基础通用配置 =====================

ENV_MODE = "prod"

BACKEND_CONFIG = {
    "host": "0.0.0.0",
    "port": 8001,
    "reload": ENV_MODE == "dev"   # ✅ 自动切换
}

API_BASE_URL = f"http://127.0.0.1:{BACKEND_CONFIG['port']}"

# ===================== 数据库 =====================

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": os.getenv("POSTGRES_DB_PASSWORD", "postgres123"),  # ✅ 环境变量优先
    "database": "ai_knowledge_base",
}

# ===================== 文本切片 =====================

TEXT_SPLIT_CONFIG = {
    "chunk_size": 500,
    "chunk_overlap": 50
}

# ===================== JWT =====================

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key")
ALGORITHM = "HS256"

# ===================== Embedding =====================

EMBEDDING_CONFIG = {
    "model_type": "qwen",   # 推荐统一
    "model_name": "text-embedding-v1",
    "dimension": 384,
    "api_key": os.getenv("QWEN_API_KEY"),
    "base_url": ""
}

# ===================== LLM =====================

LLM_CONFIG = {
    "model_type": "qwen",
    "model_name": "qwen-turbo",
    "temperature": 0.1,
    "max_tokens": 2048,
    "api_key": os.getenv("QWEN_API_KEY"),  # ✅ 核心改动
    "base_url": ""
}

# ===================== 检索 =====================

TOP_K = 3

# ===================== 历史 =====================

HISTORY_CONFIG = {
    "keep_test_data": True,
    "test_user_id": 0
}