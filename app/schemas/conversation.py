"""
    @project: aihub
    @Author: jiangkuanli
    @file: conversation
    @date: 2026/1/27
    @desc: AI对话相关的 Pydantic Schema
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class Message(BaseModel):
    """消息模型"""
    role: str = Field(..., examples=["user", "assistant"])
    content: str = Field(..., examples=["你好，请问有什么可以帮助您的？"])
    timestamp: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "你好，请问有什么可以帮助您的？",
                "timestamp": "2026-01-27T12:00:00.000000+00:00"
            }
        }


class ConversationCreate(BaseModel):
    """对话创建模型"""
    session_id: str = Field(..., examples=["会话ID"])
    title: str = Field(min_length=1, max_length=200, examples=["新对话"])
    model: Optional[str] = Field(default="gpt-3.5-turbo", examples=["gpt-3.5-turbo"])

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "会话ID",
                "title": "新对话",
                "model": "gpt-3.5-turbo"
            }
        }


class MessageCreate(BaseModel):
    """添加消息模型"""
    content: str = Field(min_length=1, max_length=5000, examples=["你好，请问有什么可以帮助您的？"])
    role: str = Field(default="user", examples=["user", "assistant"])

    class Config:
        json_schema_extra = {
            "example": {
                "content": "你好，请问有什么可以帮助您的？",
                "role": "user"
            }
        }


class ConversationResponse(BaseModel):
    """对话响应模型"""
    id: str
    session_id: str
    user_id: str
    title: str
    content: dict
    model: Optional[str]
    total_tokens: int
    is_active: bool
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True


class ConversationDetailResponse(BaseModel):
    """对话详情响应模型（包含消息列表）"""
    id: str
    session_id: str
    user_id: str
    title: str
    messages: List[Message]
    model: Optional[str]
    total_tokens: int
    is_active: bool
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True


class StreamRequest(BaseModel):
    """流式问答请求模型"""
    session_id: str = Field(..., examples=["会话ID"])
    content: str = Field(min_length=1, max_length=5000, examples=["你好，请问有什么可以帮助您的？"])
    model: str = Field(default="gpt-3.5-turbo", examples=["gpt-3.5-turbo"])

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "会话ID",
                "content": "你好，请问有什么可以帮助您的？",
                "model": "gpt-3.5-turbo"
            }
        }
