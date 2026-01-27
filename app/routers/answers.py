"""
    @project: aihub
    @Author: jiangkuanli
    @file: answers
    @date: 2026/1/27
    @desc: 答案管理接口
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.schemas.answer import AnswerCreate, AnswerResponse
from app.services.answer_service import get_answer, get_answers, create_answer, delete_answer
from app.common.core.result import Result, AppApiException
from app.models.user import User
from app.services.auth_service import get_current_user
from app.models.question import Question
from app.services.question_service import get_question as get_question_service

router = APIRouter()


@router.post("/{question_id}")
def create_answer_endpoint(
    answer_create: AnswerCreate,
    question_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新答案
    """
    question = get_question_service(db=db, question_id=question_id)
    if not question:
        raise AppApiException(404, "问题不存在")
    
    if question.user_id != current_user.id:
        raise AppApiException(403, "没有权限为其他用户的问题创建答案")
    
    return Result.success(create_answer(db=db, question_id=question_id, session_id=question.session_id, user_id=current_user.id, answer_create=answer_create)).to_dict()


@router.delete("/{answer_id}")
def delete_answer_endpoint(
    answer_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除答案
    """
    return Result.success(delete_answer(db=db, answer_id=answer_id, user_id=current_user.id)).to_dict()


@router.get("/question/{question_id}")
def get_answers_endpoint(
    question_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取问题的答案列表
    """
    question = get_question_service(db=db, question_id=question_id)
    if not question:
        raise AppApiException(404, "问题不存在")
    
    if question.user_id != current_user.id:
        raise AppApiException(403, "没有权限查看其他用户的问题答案")
    
    answers = get_answers(db=db, question_id=question_id, skip=skip, limit=limit)
    return Result.success(answers).to_dict()


@router.get("/{answer_id}")
def get_answer_endpoint(
    answer_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取答案详情
    """
    answer = get_answer(db=db, answer_id=answer_id)
    if not answer:
        raise AppApiException(404, "答案不存在")
    
    if answer.user_id != current_user.id:
        raise AppApiException(403, "没有权限查看其他用户的答案")
    
    return Result.success(answer).to_dict()
