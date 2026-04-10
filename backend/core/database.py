from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL
from sqlalchemy.dialects.postgresql.psycopg2 import PGDialect_psycopg2

from backend.config.backend_base_settings import DB_CONFIG

# 👇 关键：猴子补丁（在 create_engine 之前！）
PGDialect_psycopg2._get_server_version_info = lambda *args, **kwargs: (12, 0)

DATABASE_URL = URL.create(
    "postgresql+psycopg2",
    username=DB_CONFIG["user"],
    password=DB_CONFIG["password"],
    host=DB_CONFIG["host"],
    port=DB_CONFIG["port"],
    database=DB_CONFIG["database"]
)

engine = create_engine(
    DATABASE_URL,
    client_encoding="utf8",
    echo=True,
    pool_pre_ping=True,
    connect_args={
        "options": "-c timezone=UTC"
    }
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()