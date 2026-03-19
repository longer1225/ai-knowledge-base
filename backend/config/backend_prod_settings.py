# config/prod.py
from .backend_base_settings import *  # 导入base的所有配置

# ===================== 生产环境特有配置 =====================
ENV_MODE = "prod"

# 生产模式：关闭热重载
BACKEND_CONFIG["reload"] = False

# 生产模式：在线Embedding模型（以智谱AI为例，你可替换为OpenAI/百度等）
EMBEDDING_CONFIG["model_type"] = "online"  # 标记为在线模型
EMBEDDING_CONFIG["model_name"] = "ernie-text-embedding"  # 智谱Embedding模型
EMBEDDING_CONFIG["dimension"] = 768  # 智谱模型维度是768，覆盖base的384
EMBEDDING_CONFIG["api_key"] = "你的智谱AI API Key"  # 上线时替换为真实Key
EMBEDDING_CONFIG["base_url"] = "https://open.bigmodel.cn/api/paas/v4/"  # 智谱接口地址


# ===================== 生产环境LLM配置 =====================
LLM_CONFIG["model_type"] = "online"  # 生产用在线模型
LLM_CONFIG["model_name"] = "glm-4"  # 智谱GLM-4模型
LLM_CONFIG["api_key"] = "你的智谱AI API Key"  # 替换为真实Key
LLM_CONFIG["base_url"] = "https://open.bigmodel.cn/api/paas/v4/"  # 智谱接口地址

# config/backend_prod_settings.py
from .backend_base_settings import *

