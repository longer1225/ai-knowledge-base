from functools import wraps

from backend.core.database import SessionLocal


def db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = SessionLocal()
        try:
            result = func(*args, **kwargs, db=db)
            db.commit()   # ✅ 必须加
            return result
        except Exception as e:
            db.rollback()  # ✅ 出错回滚
            raise e
        finally:
            db.close()
    return wrapper