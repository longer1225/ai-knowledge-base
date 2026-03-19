from backend.models.user import User
from backend.utils.db_util import db_connection
from backend.utils.logger import logger


@db_connection
def get_user_by_username(username: str, db=None):
    logger.debug(f"[Mapper] 查询用户：{username}")
    return db.query(User).filter(User.username == username).first()

@db_connection
def create_mapper_user(username: str, hashed_password: str, db=None):
    logger.debug(f"[Mapper] 创建用户：{username}")
    new_user = User(
        username=username,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user