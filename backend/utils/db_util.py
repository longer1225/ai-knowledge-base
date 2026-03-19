
from functools import wraps

from backend.core.database import SessionLocal


def db_connection(func):
    """
    AOP 装饰器：自动管理数据库连接
    自动注入 db 参数
    自动打开、自动关闭
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = SessionLocal()
        try:
            # 把 db 自动注入到函数里
            return func(*args, **kwargs, db=db)
        finally:
            db.close()
    return wrapper

# 你原来的 get_db_sync 可以删掉了！