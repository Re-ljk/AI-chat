"""
    @project: aihub
    @Author: jiangkuanli
    @file: session_service
    @date: 2026/1/27
    @desc: 会话管理服务
"""

import uuid

from sqlalchemy.orm import Session

from app.common.core.result import AppApiException
from app.models import Session
from app.schemas.session import SessionCreate


def get_session(db: Session, session_id: str):
    """
    获取指定会话
    :param db: 数据库会话
    :param session_id: 会话ID
    :return: 会话对象或None
    """
    return db.query(Session).filter(Session.id == session_id).first()


def get_sessions(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    """
    获取用户的会话历史
    :param db: 数据库会话
    :param user_id: 用户ID
    :param skip: 跳过记录数
    :param limit: 限制返回记录数
    :return: 会话列表
    """
    return db.query(Session).filter(
        Session.user_id == user_id,
        Session.is_active == True
    ).offset(skip).limit(limit).order_by(Session.created_at.desc()).all()


def create_session(db: Session, user_id: str, session_create: SessionCreate):
    """
    创建新会话
    :param db: 数据库会话
    :param user_id: 用户ID
    :param session_create: 会话创建数据
    :return: 创建的会话对象
    """
    db_session = Session(
        id=str(uuid.uuid1()),
        user_id=user_id,
        session_name=session_create.session_name,
        is_active=True
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def delete_session(db: Session, session_id: str, user_id: str):
    """
    删除会话
    :param db: 数据库会话
    :param session_id: 会话ID
    :param user_id: 用户ID
    :return: 删除的会话对象
    """
    db_session = get_session(db, session_id)
    if not db_session:
        raise AppApiException(404, "会话不存在")
    
    if db_session.user_id != user_id:
        raise AppApiException(403, "没有权限删除其他用户的会话")
    
    db_session.is_active = False
    db.commit()
    db.refresh(db_session)
    return db_session
