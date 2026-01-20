"""
    @project: aihub
    @Author: dongrunhua
    @file: users
    @date: 2025/7/8 17:56
    @desc:
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.schemas.user import UserCreate
from app.services.user_service import get_user, create_user
from app.common.core.result import Result, AppApiException
from app.models.user import User
from app.services.auth_service import get_current_user

router = APIRouter()


@router.post("/")
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    # 检查当前用户是否有权限创建新用户
    if not current_user.is_superuser:
        raise AppApiException(403, message="没有权限")

    return Result.success(create_user(db=db, user=user))


@router.get("/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise AppApiException(404, message="用户不存在")
    return Result.success(db_user)


