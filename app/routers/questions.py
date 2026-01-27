"""
    @project: aihub
    @Author: jiangkuanli
    @file: questions
    @date: 2026/1/27
    @desc: 问题管理接口
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.schemas.question import QuestionCreate, QuestionResponse
from app.services.question_service import get_question, get_questions, create_question, delete_question
from app.common.core.result import Result, AppApiException
from app.models.user import User
from app.services.auth_service import get_current_user
from app.models.session import Session
from app.services.session_service import get_session

router = APIRouter()


@router.post("/{session_id}")
def create_question_endpoint(
    question_create: QuestionCreate,
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新问题
    """
    session = get_session(db=db, session_id=session_id)
    if not session:
        raise AppApiException(404, "会话不存在")
    
    if session.user_id != current_user.id:
        raise AppApiException(403, "没有权限在其他用户的会话中创建问题")
    
    return Result.success(create_question(db=db, session_id=session_id, user_id=current_user.id, question_create=question_create)).to_dict()


@router.delete("/{question_id}")
def delete_question_endpoint(
    question_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除问题
    """
    return Result.success(delete_question(db=db, question_id=question_id, user_id=current_user.id)).to_dict()


@router.get("/session/{session_id}")
def get_questions_endpoint(
    session_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取会话的问题列表
    """
    session = get_session(db=db, session_id=session_id)
    if not session:
        raise AppApiException(404, "会话不存在")
    
    if session.user_id != current_user.id:
        raise AppApiException(403, "没有权限查看其他用户的会话问题")
    
    questions = get_questions(db=db, session_id=session_id, skip=skip, limit=limit)
    return Result.success(questions).to_dict()


@router.get("/{question_id}")
def get_question_endpoint(
    question_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取问题详情
    """
    question = get_question(db=db, question_id=question_id)
    if not question:
        raise AppApiException(404, "问题不存在")
    
    if question.user_id != current_user.id:
        raise AppApiException(403, "没有权限查看其他用户的问题")
    
    return Result.success(question).to_dict()
