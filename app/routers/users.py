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
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import get_user, create_user, update_user, get_users
from app.common.core.result import Result, AppApiException
from app.models.user import User
from app.services.auth_service import get_current_user

router = APIRouter()


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return Result.success(create_user(db=db, user=user)).to_dict()


@router.put("/{user_id}")
def update_user_endpoint(
    user_id: str,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id and not current_user.is_superuser:
        raise AppApiException(403, "没有权限修改其他用户信息")

    return Result.success(update_user(db=db, user_id=user_id, user_update=user_update)).to_dict()


@router.get("/{user_id}")
def read_user(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise AppApiException(404, message="用户不存在")
    return Result.success(db_user).to_dict()


@router.get("/")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = get_users(db, skip=skip, limit=limit)
    return Result.success(users).to_dict()


