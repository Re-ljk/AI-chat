"""
    @project: aihub
    @Author: dongrunhua
    @file: document
    @date: 2026/2/4
    @desc: Document and Paragraph models for document management
"""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    content_type = Column(String)
    total_paragraphs = Column(Integer, default=0)
    chunk_size = Column(Integer)
    chunk_overlap = Column(Integer)
    splitter_type = Column(String)
    status = Column(String, default="processing")
    error_message = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    paragraphs = relationship("Paragraph", back_populates="document", cascade="all, delete-orphan")


class Paragraph(Base):
    __tablename__ = "paragraphs"

    id = Column(String, primary_key=True, index=True)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False, index=True)
    paragraph_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    character_count = Column(Integer, default=0)
    para_metadata = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    document = relationship("Document", back_populates="paragraphs")
