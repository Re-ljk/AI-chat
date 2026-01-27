"""
    @project: aihub
    @Author: jiangkuanli
    @file: answer
    @date: 2026/1/27
    @desc: 答案模型
"""

import uuid

from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.database.base import Base


class Answer(Base):
    __tablename__ = "answers"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid1()))
    question_id = Column(String, ForeignKey("questions.id"), index=True, nullable=False)
    session_id = Column(String, ForeignKey("sessions.id"), index=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    content = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
