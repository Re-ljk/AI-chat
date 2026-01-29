"""
    @project: aihub
    @Author: jiangkuanli
    @file: conversation
    @date: 2026/1/27
    @desc: AI对话模型
"""

from sqlalchemy import Boolean, Column, String, DateTime, Integer, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database.base import Base


class AIConversation(Base):
    __tablename__ = "ai_conversations"

    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), index=True, nullable=False)
    user_id = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(JSONB, nullable=False)
    model = Column(String)
    total_tokens = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
