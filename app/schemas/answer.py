"""
    @project: aihub
    @Author: jiangkuanli
    @file: answer
    @date: 2026/1/27
    @desc: 答案相关的 Pydantic Schema
"""

from typing import Optional
from pydantic import BaseModel, Field


class AnswerBase(BaseModel):
    """答案基础模型"""
    content: str = Field(min_length=1, max_length=5000, examples=["您好！我是AI助手，很高兴为您服务。"])


class AnswerCreate(AnswerBase):
    """答案创建模型"""
    class Config:
        json_schema_extra = {
            "example": {
                "content": "您好！我是AI助手，很高兴为您服务。"
            }
        }


class AnswerResponse(BaseModel):
    """答案响应模型"""
    id: str
    question_id: str
    session_id: str
    user_id: str
    content: str
    is_active: bool
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True
