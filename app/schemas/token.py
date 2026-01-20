"""
    @project: aihub
    @Author: dongrunhua
    @file: token
    @date: 2025/7/8 18:01
    @desc:
"""
from datetime import datetime
from typing import Optional

from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field


class TokenBase(BaseModel):
    """登录接口返回的Token响应模型"""
    access_token: str = Field(examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    refresh_token: str = Field(examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    token_type: str = Field(default="bearer", examples=["bearer"])
    access_expires_in: Optional[int] = Field(None, examples=[1800])
    refresh_expires_in: Optional[int] = Field(None, examples=[604800])
    is_superuser: Optional[bool] = Field(False, examples=[False])

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "access_expires_in": 1800,
                "refresh_expires_in": 604800,
                "is_superuser": False,
            }
        }


class TokenPayload(BaseModel):
    """JWT Payload 数据结构"""
    sub: str = Field(..., description="用户唯一标识（通常是email或用户ID）")
    exp: datetime = Field(..., description="过期时间")
    iat: datetime = Field(..., description="签发时间")
    jti: Optional[str] = Field(None, description="JWT ID")
    scopes: list[str] = Field(default_factory=list, description="权限范围")


class TokenData(BaseModel):
    """用于路由依赖注入的Token数据模型"""
    email: Optional[str] = None
    user_id: Optional[int] = None
    scopes: list[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "user_id": 1,
                "scopes": ["me", "items"]
            }
        }


class TokenResponse(TokenBase):
    """登录接口返回的Token响应模型"""
    access_token: str = Field(..., examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    refresh_token: Optional[str] = Field(None, examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    expires_in: int = Field(..., examples=[3600])
