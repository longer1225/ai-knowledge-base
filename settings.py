# settings.py  （纯配置，无CSS）
API_BASE_URL = "http://127.0.0.1:8000"

# GaussDB 配置
GAUSSDB_CONFIG = {
    "host": "192.168.127.128",
    "port": 5432,
    "user": "iwanna",
    "password": "56645425464ljj.",
    "database": "ai_kb",
}

# 文本切片
TEXT_SPLIT_CONFIG = {
    "chunk_size": 500,
    "chunk_overlap": 50
}

# 向量化模型
EMBEDDING_MODEL = "all-MiniLM-L6-v2"