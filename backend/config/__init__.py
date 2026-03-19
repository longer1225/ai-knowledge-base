# config/__init__.py
import os

# 读取环境变量，默认用开发环境（改环境只需改启动命令，不用改代码）
env = os.getenv("AI_ENV", "dev")

# 加载对应环境的配置
if env == "prod":
    from .backend_prod_settings import *
else:
    from .backend_dev_settings import *