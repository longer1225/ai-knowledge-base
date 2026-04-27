# backend/utils/log_util.py
from datetime import datetime
from sqlalchemy import text  # <-- 必须加这个
from backend.utils.db_util import db_connection

def clean_utf8(s: str) -> str:
    if not s:
        return ""
    return s.encode("utf-8", "ignore").decode("utf-8").strip()

@db_connection
def insert_operation_log(
    user_id: int = None,
    operation: str = "",
    module: str = "",
    content: str = "",
    ip: str = "127.0.0.1",
    db=None
):
    try:
        content = clean_utf8(content)
        operation = clean_utf8(operation)
        module = clean_utf8(module)

        # 🔥 重点：用 text() 包裹 SQL！
        sql = text("""
        INSERT INTO sys_operation_log
        (user_id, operation, module, content, ip, create_time)
        VALUES
        (:user_id, :operation, :module, :content, :ip, NOW())
        """)

        db.execute(sql, {
            "user_id": user_id,
            "operation": operation,
            "module": module,
            "content": content,
            "ip": ip
        })

    except Exception as e:
        print(f"日志写入失败: {str(e)}")