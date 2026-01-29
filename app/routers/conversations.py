"""
    @project: aihub
    @Author: jiangkuanli
    @file: conversations
    @date: 2026/1/27
    @desc: AI对话管理接口
"""

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import json

from app.database.base import get_db
from app.schemas.conversation import ConversationCreate, ConversationResponse, ConversationDetailResponse, MessageCreate, StreamMessageCreate
from app.services.conversation_service import get_conversation, get_conversations, create_conversation, delete_conversation, add_message, get_messages, add_stream_message, save_stream_message, get_red_conversations
from app.common.core.result import Result, AppApiException
from app.models.user import User
from app.services.auth_service import get_current_user

router = APIRouter()


@router.post("/")
def create_conversation_endpoint(
    conversation_create: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新对话
    """
    return Result.success(create_conversation(db=db, user_id=current_user.id, conversation_create=conversation_create)).to_dict()


@router.delete("/{conversation_id}")
def delete_conversation_endpoint(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除对话
    """
    return Result.success(delete_conversation(db=db, conversation_id=conversation_id, user_id=current_user.id)).to_dict()


@router.get("/")
def get_conversations_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取对话列表
    """
    conversations = get_conversations(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return Result.success(conversations).to_dict()


@router.get("/red")
def get_red_conversations_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取红对话列表（多轮会话）
    """
    conversations = get_red_conversations(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return Result.success(conversations).to_dict()


@router.get("/{conversation_id}")
def get_conversation_endpoint(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取对话详情
    """
    conversation = get_conversation(db=db, conversation_id=conversation_id)
    if not conversation:
        raise AppApiException(404, "对话不存在")
    
    if conversation.user_id != current_user.id:
        raise AppApiException(403, "没有权限查看其他用户的对话")
    
    return Result.success(conversation).to_dict()


@router.post("/{conversation_id}/messages")
def add_message_endpoint(
    conversation_id: str,
    message_create: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    向对话添加消息
    """
    conversation = add_message(db=db, conversation_id=conversation_id, user_id=current_user.id, message_create=message_create)
    return Result.success(conversation).to_dict()


@router.get("/{conversation_id}/messages")
def get_messages_endpoint(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取对话的消息列表
    """
    messages = get_messages(db=db, conversation_id=conversation_id, user_id=current_user.id)
    return Result.success(messages).to_dict()


@router.post("/{conversation_id}/stream")
async def stream_message_endpoint(
    conversation_id: str,
    message_create: StreamMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    流式问答接口
    """
    message_result = add_stream_message(db=db, conversation_id=conversation_id, user_id=current_user.id, message_create=message_create.dict())
    
    async def generate():
        if isinstance(message_result, dict) and "type" in message_result:
            yield json.dumps(message_result).encode('utf-8') + b'\n\n'
        else:
            yield json.dumps({
                "type": "message",
                "data": message_result
            }).encode('utf-8') + b'\n\n'
        
        yield json.dumps({
            "type": "done",
            "data": {"message": "流式响应结束"}
        }).encode('utf-8') + b'\n\n'
    
    return StreamingResponse(generate(), media_type="text/event-stream")


@router.post("/{conversation_id}/stream/save")
def save_stream_message_endpoint(
    conversation_id: str,
    message: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    保存流式消息到数据库
    """
    return Result.success(save_stream_message(db=db, conversation_id=conversation_id, user_id=current_user.id, message=message)).to_dict()
