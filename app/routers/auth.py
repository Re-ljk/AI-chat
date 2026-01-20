"""
    @project: aihub
    @Author: dongrunhua
    @file: auth
    @date: 2025/7/9 15:19
    @desc:
"""
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database.base import get_db
from app.schemas.token import TokenBase
from app.services.auth_service import authenticate_user
from app.common.core.result import AppApiException
from app.common.core.security import create_access_token, create_refresh_token
from config import settings
from app.models import User

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=TokenBase)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise AppApiException(status.HTTP_401_UNAUTHORIZED, message="用户名或密码错误",)
    # 生成短期token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    # 生成 refresh_token（长期）
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )

    return {"is_superuser": user.is_superuser, "access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer",
            "access_expires_in": access_token_expires.seconds, "refresh_expires_in": int(refresh_token_expires.total_seconds())}


@router.post("/token/refresh", response_model=TokenBase)
async def refresh_access_token(
        refresh_token: str,  # 客户端传入过期的 refresh_token
        db: Session = Depends(get_db)
):
    try:
        # 验证 refresh_token
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # 检查令牌类型（防止用 access_token 冒充）
        if payload.get("type") != "refresh":
            raise AppApiException(401, message="刷新令牌无效")
        user_email: str = payload.get("sub")
        if user_email is None:
            raise AppApiException(401, message="刷新令牌无效")
    except jwt.ExpiredSignatureError:
        raise AppApiException(401, message="刷新令牌已过期，请重新登录")
    except jwt.JWTError:
        raise AppApiException(401, message="刷新令牌无效")

    # 验证用户是否存在
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise AppApiException(status_code=401, detail="未找到用户")

    # 生成新的 access_token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    # 同时刷新 refresh_token（滑动窗口，延长有效期）
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )

    return {"is_superuser": user.is_superuser, "access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer",
            "access_expires_in": access_token_expires.seconds, "refresh_expires_in": int(refresh_token_expires.total_seconds())}
