"""
    @project: aihub
    @Author: jiangkuanli
    @file: question
    @date: 2026/1/27
    @desc: 问题模型
"""

import uuid

from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.database.base import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid1()))
    session_id = Column(String, ForeignKey("sessions.id"), index=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    content = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
