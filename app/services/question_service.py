"""
    @project: aihub
    @Author: jiangkuanli
    @file: question_service
    @date: 2026/1/27
    @desc: 问题管理服务
"""

from sqlalchemy.orm import Session

from app.common.core.result import AppApiException
from app.models import Question, Session
from app.schemas.question import QuestionCreate


def get_question(db: Session, question_id: str):
    """
    获取指定问题
    :param db: 数据库会话
    :param question_id: 问题ID
    :return: 问题对象或None
    """
    return db.query(Question).filter(Question.id == question_id).first()


def get_questions(db: Session, session_id: str, skip: int = 0, limit: int = 100):
    """
    获取会话的问题列表
    :param db: 数据库会话
    :param session_id: 会话ID
    :param skip: 跳过记录数
    :param limit: 限制返回记录数
    :return: 问题列表
    """
    return db.query(Question).filter(
        Question.session_id == session_id,
        Question.is_active == True
    ).order_by(Question.created_at.asc()).offset(skip).limit(limit).all()


def create_question(db: Session, session_id: str, user_id: str, question_create: QuestionCreate):
    """
    创建新问题
    :param db: 数据库会话
    :param session_id: 会话ID
    :param user_id: 用户ID
    :param question_create: 问题创建数据
    :return: 创建的问题对象
    """
    db_question = Question(
        session_id=session_id,
        user_id=user_id,
        content=question_create.content,
        is_active=True
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def delete_question(db: Session, question_id: str, user_id: str):
    """
    删除问题
    :param db: 数据库会话
    :param question_id: 问题ID
    :param user_id: 用户ID
    :return: 删除的问题对象
    """
    db_question = get_question(db, question_id)
    if not db_question:
        raise AppApiException(404, "问题不存在")
    
    if db_question.user_id != user_id:
        raise AppApiException(403, "没有权限删除其他用户的问题")
    
    db_question.is_active = False
    db.commit()
    db.refresh(db_question)
    return db_question
