"""
    @project: aihub
    @Author: jiangkuanli
    @file: base
    @date: 2025/7/8 17:55
    @desc:
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_engine(
    str(settings.DB_URL),
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# @contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

