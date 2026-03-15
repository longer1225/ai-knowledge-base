# API基础地址
API_BASE_URL = "http://127.0.0.1:8000"

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

# JWT配置
SECRET_KEY = "your-secret-key-keep-it-safe"
ALGORITHM = "HS256"

# 向量模型
EMBEDDING_MODEL = "all-MiniLM-L6-v2"