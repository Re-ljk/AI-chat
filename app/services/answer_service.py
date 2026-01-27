"""
    @project: aihub
    @Author: jiangkuanli
    @file: answer_service
    @date: 2026/1/27
    @desc: 答案管理服务
"""

from sqlalchemy.orm import Session

from app.common.core.result import AppApiException
from app.models import Answer, Question
from app.schemas.answer import AnswerCreate


def get_answer(db: Session, answer_id: str):
    """
    获取指定答案
    :param db: 数据库会话
    :param answer_id: 答案ID
    :return: 答案对象或None
    """
    return db.query(Answer).filter(Answer.id == answer_id).first()


def get_answers(db: Session, question_id: str, skip: int = 0, limit: int = 100):
    """
    获取问题的答案列表
    :param db: 数据库会话
    :param question_id: 问题ID
    :param skip: 跳过记录数
    :param limit: 限制返回记录数
    :return: 答案列表
    """
    return db.query(Answer).filter(
        Answer.question_id == question_id,
        Answer.is_active == True
    ).order_by(Answer.created_at.asc()).offset(skip).limit(limit).all()


def create_answer(db: Session, question_id: str, session_id: str, user_id: str, answer_create: AnswerCreate):
    """
    创建新答案
    :param db: 数据库会话
    :param question_id: 问题ID
    :param session_id: 会话ID
    :param user_id: 用户ID
    :param answer_create: 答案创建数据
    :return: 创建的答案对象
    """
    db_answer = Answer(
        question_id=question_id,
        session_id=session_id,
        user_id=user_id,
        content=answer_create.content,
        is_active=True
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def delete_answer(db: Session, answer_id: str, user_id: str):
    """
    删除答案
    :param db: 数据库会话
    :param answer_id: 答案ID
    :param user_id: 用户ID
    :return: 删除的答案对象
    """
    db_answer = get_answer(db, answer_id)
    if not db_answer:
        raise AppApiException(404, "答案不存在")
    
    if db_answer.user_id != user_id:
        raise AppApiException(403, "没有权限删除其他用户的答案")
    
    db_answer.is_active = False
    db.commit()
    db.refresh(db_answer)
    return db_answer
