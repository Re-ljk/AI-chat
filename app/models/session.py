"""
    @project: aihub
    @Author: jiangkuanli
    @file: session
    @date: 2026/1/27
    @desc: 会话模型
"""

from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.base import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    session_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
