# 🔥 保留你原来所有逻辑！
# 🔥 只调整导入顺序！
# 🔥 不写死！不破坏！

# 1. 先导入 base（但不提取 ENV_MODE）
from . import backend_base_settings

# 2. 读取 base 里的环境变量
ENV_MODE = backend_base_settings.ENV_MODE

# 3. 根据环境加载配置
if ENV_MODE == "prod":
    from .backend_prod_settings import *
else:
    from .backend_dev_settings import *