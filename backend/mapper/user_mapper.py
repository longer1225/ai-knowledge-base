# backend/mapper/user_mapper.py
from backend.models import User
from utils.db_util import db_connection

# 自动有 db！不用开、不用关！
@db_connection
def get_user_by_username(username: str, db=None):
    return db.query(User).filter(User.username == username).first()

@db_connection
def create_mapper_user(username: str, hashed_password: str, db=None):
    new_user = User(
        username=username,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user