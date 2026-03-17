# utils/logger.py
import logging
import sys
from config.backend_base_settings import ENV_MODE


def get_logger(name: str = "ai_knowledge_base"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # 控制台输出
    console_handler = logging.StreamHandler(sys.stdout)

    # 开发环境输出DEBUG，生产环境只输出INFO及以上
    if ENV_MODE == "dev":
        console_handler.setLevel(logging.DEBUG)
    else:
        console_handler.setLevel(logging.INFO)

    # 日志格式
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


# 全局导出，直接用这个
logger = get_logger()