import os
import time
import threading
from pathlib import Path

from backend.service.upload_service import upload_document
from fastapi import UploadFile
from backend.utils.logger import logger
from backend.utils.log_util import insert_operation_log  # 加这一行

# ==============================
# 目录配置
# ==============================
BASE_DIR = Path(__file__).parent.parent.parent
AUTO_UPLOAD_DIR = BASE_DIR / "auto_upload"
COMPLETED_DIR = AUTO_UPLOAD_DIR / "completed"
FAILED_DIR = AUTO_UPLOAD_DIR / "failed"

AUTO_UPLOAD_DIR.mkdir(exist_ok=True)
COMPLETED_DIR.mkdir(exist_ok=True)
FAILED_DIR.mkdir(exist_ok=True)

# ==============================
# 支持格式
# ==============================
ALLOWED_TYPES = {"txt", "md", "docx", "pdf", "csv", "pptx"}


def process_file(file_path: Path, user_id: int = 1):
    """处理单个文件（防重复 + 安全移动）"""

    filename = file_path.name
    suffix = file_path.suffix.lower().replace(".", "")

    # ======================
    # 跳过非法文件
    # ======================
    if suffix not in ALLOWED_TYPES:
        logger.info(f"[自动上传] 跳过不支持的文件: {filename}")
        return

    # ======================
    # 🔥 防重复处理（核心）
    # ======================
    processing_path = file_path.with_suffix(file_path.suffix + ".processing")

    try:
        # 重命名为 processing 状态
        file_path.rename(processing_path)
    except Exception:
        # 说明已经被其他线程/轮处理
        return

    logger.info(f"[自动上传] 开始处理: {filename}")

    try:
        # ======================
        # 构造 UploadFile
        # ======================
        with open(processing_path, "rb") as f:
            upload_file = UploadFile(
                filename=filename,
                file=f
            )

            doc_id = upload_document(upload_file, user_id)

        logger.info(f"[自动上传] 处理完成！doc_id={doc_id} -> {filename}")

        insert_operation_log(
            user_id=user_id,
            operation="自动上传文档",
            module="文档知识库",
            content=f"自动上传文件：{filename}，文档ID：{doc_id}"
        )

        # ======================
        # 移动到 completed
        # ======================
        dest = COMPLETED_DIR / filename

        # 防重名
        if dest.exists():
            dest = COMPLETED_DIR / f"{int(time.time())}_{filename}"

        processing_path.rename(dest)

        logger.info(f"[自动上传] 文件已归档: {dest.name}\n")

    except Exception as e:
        logger.error(f"[自动上传] 处理失败: {filename} | {str(e)}")

        # ======================
        # 移动到 failed
        # ======================
        failed_dest = FAILED_DIR / filename

        if failed_dest.exists():
            failed_dest = FAILED_DIR / f"{int(time.time())}_{filename}"

        try:
            processing_path.rename(failed_dest)
        except Exception:
            logger.error(f"[自动上传] 文件移动到 failed 失败: {filename}")


def scan_loop(interval: int = 10, user_id: int = 1):
    """循环扫描目录"""

    logger.info("=" * 60)
    logger.info(f"🚀 自动文件扫描服务已启动 | 每{interval}秒扫描一次")
    logger.info(f"📂 监控目录: {AUTO_UPLOAD_DIR}")
    logger.info("=" * 60)

    while True:
        try:
            for f in AUTO_UPLOAD_DIR.iterdir():
                if (
                    f.is_file()
                    and not f.name.startswith(".")
                    and not f.name.endswith(".processing")  # 🔥 防止重复
                ):
                    process_file(f, user_id)

        except Exception as e:
            logger.error(f"[扫描循环] 异常: {str(e)}")

        time.sleep(interval)


def start_auto_upload_scanner(user_id: int = 1):
    """启动后台线程"""

    t = threading.Thread(
        target=scan_loop,
        kwargs={"user_id": user_id},
        daemon=True
    )
    t.start()