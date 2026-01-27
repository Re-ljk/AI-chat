"""
    @project: aihub
    @Author: jiangkuanli
    @file: session
    @date: 2026/1/27
    @desc: 会话相关的 Pydantic Schema
"""

from typing import Optional
from pydantic import BaseModel, Field


class SessionBase(BaseModel):
    """会话基础模型"""
    session_name: str = Field(min_length=1, max_length=100, examples=["新会话"])


class SessionCreate(SessionBase):
    """会话创建模型"""
    class Config:
        json_schema_extra = {
            "example": {
                "session_name": "新会话"
            }
        }


class SessionResponse(BaseModel):
    """会话响应模型"""
    id: str
    user_id: str
    session_name: str
    is_active: bool
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True
