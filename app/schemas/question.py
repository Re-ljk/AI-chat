"""
    @project: aihub
    @Author: jiangkuanli
    @file: question
    @date: 2026/1/27
    @desc: 问题相关的 Pydantic Schema
"""

from typing import Optional
from pydantic import BaseModel, Field


class QuestionBase(BaseModel):
    """问题基础模型"""
    content: str = Field(min_length=1, max_length=5000, examples=["你好，请问有什么可以帮助您的？"])


class QuestionCreate(QuestionBase):
    """问题创建模型"""
    class Config:
        json_schema_extra = {
            "example": {
                "content": "你好，请问有什么可以帮助您的？"
            }
        }


class QuestionResponse(BaseModel):
    """问题响应模型"""
    id: str
    session_id: str
    user_id: str
    content: str
    is_active: bool
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True
