# config/dev.py
from .backend_base_settings import *  # 导入base的所有配置

# ===================== 开发环境特有配置 =====================

# 开发模式：开启热重载
BACKEND_CONFIG["reload"] = True

# 开发模式：本地开源Embedding模型（不用API，免费调试）
EMBEDDING_CONFIG["model_type"] = "mock"  # 标记为本地模型
EMBEDDING_CONFIG["model_name"] = "all-MiniLM-L6-v2"  # 轻量开源模型
# dimension继承base的384，不用改
# api_key继承base的空值，不用改

# ===================== 开发环境LLM配置 =====================
LLM_CONFIG["model_type"] = "mock"  # 开发用假模型/本地开源模型
LLM_CONFIG["model_name"] = "fake-llm"  # 标记为假模型
LLM_CONFIG["local_model_path"] = "./models/llm/ollama_qwen2"  # 本地Ollama模型路径（可选）

# config/backend_dev_settings.py
from .backend_base_settings import *

# 原有配置不变，新增/修改历史记录配置
HISTORY_CONFIG["keep_test_data"] = True  # 开发环境保留测试数据
HISTORY_CONFIG["test_user_id"] = 1       # 测试用户ID（比如你的开发账号ID）