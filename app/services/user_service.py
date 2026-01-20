"""
    @project: aihub
    @Author: dongrunhua
    @file: user_service
    @date: 2025/7/8 17:57
    @desc:
"""
import base64
import uuid

from sqlalchemy.orm import Session, joinedload

from app.common.core.result import AppApiException
from app.common.core.security import get_password_hash
from app.models import User
from app.schemas.user import UserCreate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    if db.query(User).filter(User.email == user.email).first():
        raise AppApiException(500, "邮箱已被注册")

    hashed_password = get_password_hash(user.password)
    db_user = User(
        id=str(uuid.uuid1()),
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
