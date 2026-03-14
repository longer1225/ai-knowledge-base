# API基础地址
API_BASE_URL = "http://127.0.0.1:8000"

# Docker PostgreSQL 配置（替换原GaussDB配置）
GAUSSDB_CONFIG = {
    "host": "localhost",  # Docker容器映射的本地地址
    "port": 5432,
    "user": "postgres",   # Docker PostgreSQL默认用户
    "password": "Postgres@123",  # 你设置的密码
    "database": "qa_knowledge_system",  # 你新建的项目库
}

# 文本切片配置
TEXT_SPLIT_CONFIG = {
    "chunk_size": 500,
    "chunk_overlap": 50
}

# JWT配置
SECRET_KEY = "your-secret-key-keep-it-safe"  # 建议用openssl rand -hex 32生成随机串
ALGORITHM = "HS256"

# 向量化模型
EMBEDDING_MODEL = "all-MiniLM-L6-v2"