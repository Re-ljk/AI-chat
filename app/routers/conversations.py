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
from app.schemas.conversation import ConversationCreate, ConversationResponse, ConversationDetailResponse, MessageCreate, StreamMessageCreate, ConversationUpdate
from app.services.conversation_service import get_conversation, get_conversations, create_conversation, delete_conversation, add_message, get_messages, add_stream_message, save_stream_message, get_red_conversations, generate_ai_response_with_langchain, summarize_conversation_with_langchain, get_conversation_context, is_langchain_initialized, update_conversation
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


@router.put("/{conversation_id}")
def update_conversation_endpoint(
    conversation_id: str,
    conversation_update: ConversationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新对话
    """
    conversation = update_conversation(db=db, conversation_id=conversation_id, user_id=current_user.id, conversation_update=conversation_update)
    return Result.success(conversation).to_dict()


@router.get("/langchain/status")
def get_langchain_status_endpoint(
    current_user: User = Depends(get_current_user)
):
    """
    获取LangChain服务状态
    """
    return Result.success({
        "initialized": is_langchain_initialized(),
        "message": "LangChain服务已初始化" if is_langchain_initialized() else "LangChain服务未初始化，请检查API密钥配置"
    }).to_dict()


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
        
        # 生成AI回复
        conversation = get_conversation(db=db, conversation_id=conversation_id)
        if conversation:
            # 获取对话历史
            conversation_history = conversation.content or []
            
            # 使用LangChain生成AI回复
            ai_result = await generate_ai_response_with_langchain(
                conversation_history=conversation_history,
                user_message=message_create.content
            )
            
            if ai_result["success"]:
                ai_response = ai_result["response"]
                
                # 模拟流式返回
                for i in range(0, len(ai_response), 50):
                    chunk = ai_response[i:i+50]
                    yield json.dumps({
                        "type": "message",
                        "data": {
                            "role": "assistant",
                            "content": chunk
                        }
                    }).encode('utf-8') + b'\n\n'
                
                yield json.dumps({
                    "type": "done",
                    "data": {
                        "message": "流式响应结束",
                        "content": ai_response
                    }
                }).encode('utf-8') + b'\n\n'
            else:
                yield json.dumps({
                    "type": "error",
                    "data": {
                        "code": 500,
                        "message": ai_result["error"] or "生成AI回复失败"
                    }
                }).encode('utf-8') + b'\n\n'
        else:
            yield json.dumps({
                "type": "error",
                "data": {
                    "code": 404,
                    "message": "对话不存在"
                }
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


@router.post("/{conversation_id}/ai-response")
async def generate_ai_response_endpoint(
    conversation_id: str,
    message_create: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    使用LangChain生成AI回复（基于对话历史）
    """
    conversation = get_conversation(db=db, conversation_id=conversation_id)
    if not conversation:
        raise AppApiException(404, "对话不存在")
    
    if conversation.user_id != current_user.id:
        raise AppApiException(403, "没有权限查看其他用户的对话")
    
    conversation_history = conversation.content or []
    
    result = await generate_ai_response_with_langchain(
        conversation_history=conversation_history,
        user_message=message_create.content
    )
    
    if result["success"]:
        return Result.success({
            "response": result["response"],
            "memory_used": result["memory_used"]
        }).to_dict()
    else:
        raise AppApiException(500, f"AI回复生成失败: {result['error']}")


@router.get("/{conversation_id}/summary")
async def get_conversation_summary_endpoint(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取对话总结（使用LangChain）
    """
    conversation = get_conversation(db=db, conversation_id=conversation_id)
    if not conversation:
        raise AppApiException(404, "对话不存在")
    
    if conversation.user_id != current_user.id:
        raise AppApiException(403, "没有权限查看其他用户的对话")
    
    conversation_history = conversation.content or []
    
    summary_result = await summarize_conversation_with_langchain(conversation_history=conversation_history)
    
    if summary_result["success"]:
        return Result.success({
            "summary": summary_result["summary"],
            "message_count": summary_result["message_count"]
        }).to_dict()
    else:
        raise AppApiException(500, f"对话总结失败: {summary_result['error']}")


@router.get("/{conversation_id}/context")
async def get_conversation_context_endpoint(
    conversation_id: str,
    max_context_length: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取对话上下文（使用LangChain）
    """
    conversation = get_conversation(db=db, conversation_id=conversation_id)
    if not conversation:
        raise AppApiException(404, "对话不存在")
    
    if conversation.user_id != current_user.id:
        raise AppApiException(403, "没有权限查看其他用户的对话")
    
    conversation_history = conversation.content or []
    
    context_result = await get_conversation_context(
        conversation_history=conversation_history,
        max_context_length=max_context_length
    )
    
    if context_result["success"]:
        return Result.success({
            "context": context_result["context"],
            "message_count": context_result["message_count"],
            "max_context_length": context_result["max_context_length"]
        }).to_dict()
    else:
        raise AppApiException(500, f"获取对话上下文失败: {context_result['error']}")


@router.get("/langchain/status")
def get_langchain_status_endpoint(
    current_user: User = Depends(get_current_user)
):
    """
    获取LangChain服务状态
    """
    return Result.success({
        "initialized": is_langchain_initialized(),
        "message": "LangChain服务已初始化" if is_langchain_initialized() else "LangChain服务未初始化，请检查API密钥配置"
    }).to_dict()
