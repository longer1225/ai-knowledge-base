from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import GAUSSDB_CONFIG

DB_URL = f"postgresql+psycopg2://{GAUSSDB_CONFIG['user']}:{GAUSSDB_CONFIG['password']}@{GAUSSDB_CONFIG['host']}:{GAUSSDB_CONFIG['port']}/{GAUSSDB_CONFIG['database']}"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 给 FastAPI 依赖用
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 你定义的：close_db()
def close_db(db):
    db.close()