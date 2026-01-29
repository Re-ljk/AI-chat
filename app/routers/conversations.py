"""
    @project: aihub
    @Author: jiangkuanli
    @file: conversations
    @date: 2026/1/27
    @desc: AI对话管理接口
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json

from app.database.base import get_db
from app.schemas.conversation import ConversationCreate, ConversationResponse, ConversationDetailResponse, MessageCreate, StreamRequest
from app.services.conversation_service import get_conversation, get_conversations, create_conversation, delete_conversation, add_message, get_messages, stream_chat
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


@router.post("/stream")
async def stream_chat_endpoint(
    stream_request: StreamRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    流式问答接口
    """
    from fastapi.responses import StreamingResponse
    
    conversation = stream_chat(db=db, session_id=stream_request.session_id, user_id=current_user.id, stream_request=stream_request)
    
    async def generate():
        yield f"data: {json.dumps({'type': 'start', 'conversation': conversation.to_dict()}, ensure_ascii=False)}\n\n"
        
        yield f"data: {json.dumps({'type': 'message', 'message': {'role': 'user', 'content': stream_request.content}}, ensure_ascii=False)}\n\n"
        
        yield f"data: {json.dumps({'type': 'message', 'message': {'role': 'assistant', 'content': '这是一个模拟的AI回复'}}, ensure_ascii=False)}\n\n"
        
        yield f"data: {json.dumps({'type': 'end'}, ensure_ascii=False)}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")
