# API基础地址
# config.py
API_BASE_URL = "http://127.0.0.1:8001"

# PostgreSQL配置
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

# 随便写一串密钥就行
SECRET_KEY = "1234567890abcdefghijklmnopqrstuvwxyz"
ALGORITHM = "HS256"
# 向量模型
# 嵌入模型配置（切换模型只改这里！）
EMBEDDING_CONFIG = {
    "model_type": "mock",    # 👈 就改这一行！
    "dimension": 384,
    # "api_key": "xxx",        # 未来在线模型用
}

# settings.py

# 环境配置：专业开发标准！
# dev  = 开发模式（不调用LLM，不花钱，适合调试）
# prod = 生产模式（正式运行，调用LLM）
ENV_MODE = "dev"  # 你只改这里！全局生效！