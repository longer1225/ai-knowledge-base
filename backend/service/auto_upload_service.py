import os
import time
import threading
from pathlib import Path
from utils.logger import logger
from backend.service.upload_service import upload_document
from fastapi import UploadFile

# 配置目录
BASE_DIR = Path(__file__).parent.parent.parent
AUTO_UPLOAD_DIR = BASE_DIR / "auto_upload"
COMPLETED_DIR = AUTO_UPLOAD_DIR / "completed"

# 自动创建目录
AUTO_UPLOAD_DIR.mkdir(exist_ok=True)
COMPLETED_DIR.mkdir(exist_ok=True)

# 支持的格式
ALLOWED_TYPES = {"txt", "md", "pdf"}


def process_file(file_path: Path, user_id: int = 1):
    """自动处理单个文件，直接调用你现有的上传逻辑"""
    try:
        filename = file_path.name
        suffix = file_path.suffix.lower().replace(".", "")

        if suffix not in ALLOWED_TYPES:
            logger.info(f"[自动上传] 跳过不支持的文件: {filename}")
            return

        logger.info(f"[自动上传] 开始处理: {filename}")

        # 封装成 FastAPI UploadFile 对象（完全兼容你现有代码）
        with open(file_path, "rb") as f:
            upload_file = UploadFile(
                filename=filename,
                file=f
            )
            # 直接调用你写好的方法！
            doc_id = upload_document(upload_file, user_id)

        logger.info(f"[自动上传] 处理完成！doc_id={doc_id} -> {filename}")

        # 移动到已完成目录
        dest = COMPLETED_DIR / filename
        file_path.rename(dest)
        logger.info(f"[自动上传] 文件已归档: {dest.name}\n")

    except Exception as e:
        logger.error(f"[自动上传] 处理失败: {file_path.name} | {str(e)}")


def scan_loop(interval: int = 10, user_id: int = 1):
    """无限循环扫描目录"""
    logger.info("=" * 60)
    logger.info(f"🚀 自动文件扫描服务已启动 | 每{interval}秒扫描一次")
    logger.info(f"📂 监控目录: {AUTO_UPLOAD_DIR}")
    logger.info("=" * 60)

    while True:
        try:
            # 遍历目录所有文件
            for f in AUTO_UPLOAD_DIR.iterdir():
                if f.is_file() and not f.name.startswith("."):
                    process_file(f, user_id)

        except Exception as e:
            logger.error(f"[扫描循环] 异常: {str(e)}")

        time.sleep(interval)


def start_auto_upload_scanner(user_id: int = 1):
    """后台线程启动扫描"""
    t = threading.Thread(
        target=scan_loop,
        kwargs={"user_id": user_id},
        daemon=True
    )
    t.start()