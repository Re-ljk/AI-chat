"""
    @project: aihub
    @Author: jiangkuanli
    @file: conversation_service
    @date: 2026/1/27
    @desc: AI对话管理服务
"""

import uuid
from datetime import datetime
from sqlalchemy.orm import Session

from app.common.core.result import AppApiException
from app.models import AIConversation
from app.schemas.conversation import ConversationCreate, MessageCreate


def get_conversation(db: Session, conversation_id: str):
    """
    获取指定对话
    :param db: 数据库会话
    :param conversation_id: 对话ID
    :return: 对话对象或None
    """
    return db.query(AIConversation).filter(AIConversation.id == conversation_id).first()


def get_conversations(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    """
    获取用户的对话列表
    :param db: 数据库会话
    :param user_id: 用户ID
    :param skip: 跳过记录数
    :param limit: 限制返回记录数
    :return: 对话列表
    """
    return db.query(AIConversation).filter(
        AIConversation.user_id == user_id,
        AIConversation.is_active == True
    ).order_by(AIConversation.created_at.desc()).offset(skip).limit(limit).all()


def create_conversation(db: Session, user_id: str, conversation_create: ConversationCreate):
    """
    创建新对话
    :param db: 数据库会话
    :param user_id: 用户ID
    :param conversation_create: 对话创建数据
    :return: 创建的对话对象
    """
    db_conversation = AIConversation(
        id=str(uuid.uuid1()),
        user_id=user_id,
        title=conversation_create.title,
        model=conversation_create.model,
        content=[],
        total_tokens=0,
        is_active=True
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation


def delete_conversation(db: Session, conversation_id: str, user_id: str):
    """
    删除对话
    :param db: 数据库会话
    :param conversation_id: 对话ID
    :param user_id: 用户ID
    :return: 删除的对话对象
    """
    db_conversation = get_conversation(db, conversation_id)
    if not db_conversation:
        raise AppApiException(404, "对话不存在")
    
    if db_conversation.user_id != user_id:
        raise AppApiException(403, "没有权限删除其他用户的对话")
    
    db_conversation.is_active = False
    db.commit()
    db.refresh(db_conversation)
    return db_conversation


def add_message(db: Session, conversation_id: str, user_id: str, message_create: MessageCreate):
    """
    向对话添加消息
    :param db: 数据库会话
    :param conversation_id: 对话ID
    :param user_id: 用户ID
    :param message_create: 消息创建数据
    :return: 更新后的对话对象
    """
    db_conversation = get_conversation(db, conversation_id)
    if not db_conversation:
        raise AppApiException(404, "对话不存在")
    
    if db_conversation.user_id != user_id:
        raise AppApiException(403, "没有权限向其他用户的对话添加消息")
    
    message = {
        "role": message_create.role,
        "content": message_create.content,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if db_conversation.content is None:
        db_conversation.content = []
    
    db_conversation.content.append(message)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation


def get_messages(db: Session, conversation_id: str, user_id: str):
    """
    获取对话的消息列表
    :param db: 数据库会话
    :param conversation_id: 对话ID
    :param user_id: 用户ID
    :return: 消息列表
    """
    db_conversation = get_conversation(db, conversation_id)
    if not db_conversation:
        raise AppApiException(404, "对话不存在")
    
    if db_conversation.user_id != user_id:
        raise AppApiException(403, "没有权限查看其他用户的对话消息")
    
    return db_conversation.content or []


def add_stream_message(db: Session, conversation_id: str, user_id: str, message_create: dict):
    """
    向对话添加流式消息（不立即保存到数据库）
    :param db: 数据库会话
    :param conversation_id: 对话ID
    :param user_id: 用户ID
    :param message_create: 消息创建数据
    :return: 消息对象或错误信息
    """
    db_conversation = get_conversation(db, conversation_id)
    if not db_conversation:
        return {
            "type": "error",
            "data": {
                "code": 404,
                "message": "对话不存在"
            }
        }
    
    if db_conversation.user_id != user_id:
        return {
            "type": "error",
            "data": {
                "code": 403,
                "message": "没有权限向其他用户的对话添加消息"
            }
        }
    
    message = {
        "role": message_create.get("role", "user"),
        "content": message_create.get("content", ""),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    return message


def save_stream_message(db: Session, conversation_id: str, user_id: str, message: dict):
    """
    保存流式消息到数据库
    :param db: 数据库会话
    :param conversation_id: 对话ID
    :param user_id: 用户ID
    :param message: 消息对象
    :return: 更新后的对话对象
    """
    from sqlalchemy.orm.attributes import flag_modified
    
    db_conversation = get_conversation(db, conversation_id)
    if not db_conversation:
        raise AppApiException(404, "对话不存在")
    
    if db_conversation.user_id != user_id:
        raise AppApiException(403, "没有权限向其他用户的对话添加消息")
    
    if db_conversation.content is None:
        db_conversation.content = []
    
    db_conversation.content.append(message)
    flag_modified(db_conversation, "content")
    db.commit()
    db.refresh(db_conversation)
    return db_conversation


def get_red_conversations(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    """
    获取用户的红对话列表（多轮会话）
    :param db: 数据库会话
    :param user_id: 用户ID
    :param skip: 跳过记录数
    :param limit: 限制返回记录数
    :return: 对话列表
    """
    return db.query(AIConversation).filter(
        AIConversation.user_id == user_id,
        AIConversation.is_active == True
    ).order_by(AIConversation.updated_at.desc()).offset(skip).limit(limit).all()
