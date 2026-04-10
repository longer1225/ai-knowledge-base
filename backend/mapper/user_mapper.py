from backend.models.user import User
from backend.utils.db_util import db_connection
from backend.utils.orm_to_dict_util import to_dict
from backend.utils.logger import logger


@db_connection
def get_user_by_username(username: str, db=None):
    logger.debug(f"[Mapper] 查询用户：{username}")
    user = db.query(User).filter(User.username == username).first()

    # 自动转换 字典/None
    return to_dict(user)


@db_connection
def create_mapper_user(username: str, hashed_password: str, db=None):
    logger.debug(f"[Mapper] 创建用户：{username}")
    new_user = User(
        username=username,
        password=hashed_password
    )
    db.add(new_user)
    db.flush()
    db.refresh(new_user)

    # 自动转换
    return to_dict(new_user)