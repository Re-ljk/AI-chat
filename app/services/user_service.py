"""
    @project: aihub
    @Author: jiangkuanli
    @file: user_service
    @date: 2026/2/4
    @desc:
"""
import base64
import uuid

from sqlalchemy.orm import Session, joinedload

from app.common.core.result import AppApiException
from app.common.core.security import get_password_hash, verify_password
from app.models import User
from app.schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    if db.query(User).filter(User.email == user.email).first():
        raise AppApiException(500, "邮箱已被注册")
    
    if db.query(User).filter(User.username == user.username).first():
        raise AppApiException(500, "用户名已被注册")

    hashed_password = get_password_hash(user.password)
    db_user = User(
        id=str(uuid.uuid1()),
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: str, user_update: UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        raise AppApiException(404, "用户不存在")

    if user_update.full_name is not None:
        db_user.full_name = user_update.full_name

    if user_update.password is not None:
        db_user.hashed_password = get_password_hash(user_update.password)

    db.commit()
    db.refresh(db_user)
    return db_user
