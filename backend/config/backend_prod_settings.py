# config/backend_prod_settings.py
from .backend_base_settings import *

# ===================== 生产环境特有配置 =====================
BACKEND_CONFIG["reload"] = False

# ===================== 生产环境：阿里云通义千问 =====================
LLM_CONFIG["model_type"] = "qwen"             # ✅ 必须是 qwen
LLM_CONFIG["model_name"] = "qwen-turbo"       # ✅ 阿里云免费模型
LLM_CONFIG["temperature"] = 0.1
LLM_CONFIG["max_tokens"] = 2048
LLM_CONFIG["base_url"] = ""                   # ✅ 留空

# ===================== 嵌入模型（可选，暂时用 mock 不影响） =====================
# ===================== 嵌入模型（必须改这里） =====================
EMBEDDING_CONFIG["model_type"] = "qwen"   # 🔥 改这里
EMBEDDING_CONFIG["model_name"] = "text-embedding-v1"
EMBEDDING_CONFIG["base_url"] = ""