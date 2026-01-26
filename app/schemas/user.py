"""
    @project: aihub
    @Author: dongrunhua
    @file: user
    @date: 2025/7/8 17:56
    @desc:
"""

from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """用户基础模型"""
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",  examples=["user@example.com"],)
    full_name: Optional[str] = Field(examples=["张三"])


class UserCreate(UserBase):
    """用户创建模型（注册用）"""
    password: str = Field(min_length=6, examples=["strongpassword123"])

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "full_name": "张三",
                "password": "strongpassword123"
            }
        }


class UserUpdate(BaseModel):
    """用户更新模型（修改信息用）"""
    full_name: Optional[str] = Field(None, examples=["李四"])
    password: Optional[str] = Field(None, min_length=6, examples=["newpassword123"])

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "李四",
                "password": "newpassword123"
            }
        }


class UserResponse(BaseModel):
    """用户响应模型"""
    id: str
    email: str
    full_name: Optional[str]
    is_active: bool
    is_superuser: bool
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True
