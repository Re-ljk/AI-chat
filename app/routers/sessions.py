"""
    @project: aihub
    @Author: jiangkuanli
    @file: sessions
    @date: 2026/1/27
    @desc: 会话管理接口
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.schemas.session import SessionCreate, SessionResponse
from app.services.session_service import get_session, get_sessions, create_session, delete_session
from app.common.core.result import Result, AppApiException
from app.models.user import User
from app.services.auth_service import get_current_user

router = APIRouter()


@router.post("/")
def create_session_endpoint(
    session_create: SessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新会话
    """
    return Result.success(create_session(db=db, user_id=current_user.id, session_create=session_create)).to_dict()


@router.delete("/{session_id}")
def delete_session_endpoint(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除会话
    """
    return Result.success(delete_session(db=db, session_id=session_id, user_id=current_user.id)).to_dict()


@router.get("/")
def get_sessions_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取会话历史
    """
    sessions = get_sessions(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return Result.success(sessions).to_dict()


@router.get("/{session_id}")
def get_session_endpoint(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取会话详情
    """
    session = get_session(db=db, session_id=session_id)
    if not session:
        raise AppApiException(404, "会话不存在")
    
    if session.user_id != current_user.id:
        raise AppApiException(403, "没有权限查看其他用户的会话")
    
    return Result.success(session).to_dict()
