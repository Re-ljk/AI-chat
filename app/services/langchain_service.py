"""
    @project: aihub
    @Author: jiangkuanli
    @file: langchain_service
    @date: 2026/1/29
    @desc: LangChain集成服务，实现对话历史学习
"""

from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

from config import settings


class LangChainService:
    """
    LangChain服务类，提供对话历史学习和上下文管理功能
    """
    
    def __init__(self):
        """
        初始化LangChain服务
        """
        self.llm = None
        
        # 如果配置了DeepSeek API密钥，则初始化LLM
        if hasattr(settings, 'DEEPSEEK_API_KEY') and settings.DEEPSEEK_API_KEY:
            self._initialize_deepseek()
    
    def _initialize_deepseek(self):
        """
        初始化DeepSeek LLM
        """
        try:
            self.llm = ChatOpenAI(
                openai_api_key=settings.DEEPSEEK_API_KEY,
                base_url=settings.DEEPSEEK_BASE_URL,
                model=settings.DEEPSEEK_MODEL,
                temperature=0.7
            )
            print("DeepSeek LLM初始化成功")
        except Exception as e:
            print(f"DeepSeek LLM初始化失败: {e}")
    
    async def generate_response(
        self,
        user_message: str,
        conversation_history: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        基于对话历史生成AI回复
        
        :param user_message: 用户消息
        :param conversation_history: 对话历史
        :return: 包含AI回复和元数据的字典
        """
        try:
            if not self.llm:
                return {
                    "success": False,
                    "response": None,
                    "memory_used": len(conversation_history) if conversation_history else 0,
                    "error": "LLM未初始化，请配置DEEPSEEK_API_KEY"
                }
            
            # 构建消息列表
            messages = []
            
            if conversation_history:
                for msg in conversation_history:
                    if msg.get('role') == 'user':
                        messages.append(HumanMessage(content=msg.get('content', '')))
                    elif msg.get('role') == 'assistant':
                        messages.append(AIMessage(content=msg.get('content', '')))
            
            messages.append(HumanMessage(content=user_message))
            
            # 生成回复
            response = await self.llm.ainvoke(messages)
            
            return {
                "success": True,
                "response": response.content,
                "memory_used": len(conversation_history) if conversation_history else 0,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "response": None,
                "memory_used": len(conversation_history) if conversation_history else 0,
                "error": str(e)
            }
    
    async def summarize_conversation(
        self,
        conversation_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        对话总结
        
        :param conversation_history: 对话历史
        :return: 包含总结和元数据的字典
        """
        try:
            if not self.llm:
                return {
                    "success": False,
                    "summary": None,
                    "message_count": len(conversation_history),
                    "error": "LLM未初始化，请配置DEEPSEEK_API_KEY"
                }
            
            # 构建对话文本
            conversation_text = "\n".join([
                f"{msg.get('role', 'user')}: {msg.get('content', '')}"
                for msg in conversation_history
            ])
            
            # 生成总结
            messages = [
                SystemMessage(content="你是一个对话总结专家。请用中文总结以下对话的主要内容。"),
                HumanMessage(content=f"请总结以下对话：\n\n{conversation_text}")
            ]
            
            response = await self.llm.ainvoke(messages)
            
            return {
                "success": True,
                "summary": response.content,
                "message_count": len(conversation_history),
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "summary": None,
                "message_count": len(conversation_history),
                "error": str(e)
            }
    
    async def get_context(
        self,
        conversation_history: List[Dict[str, Any]],
        max_context_length: int = 10
    ) -> Dict[str, Any]:
        """
        获取对话上下文
        
        :param conversation_history: 对话历史
        :param max_context_length: 最大上下文长度
        :return: 包含上下文和元数据的字典
        """
        try:
            # 获取最近的对话
            recent_conversation = conversation_history[-max_context_length:]
            
            # 构建上下文文本
            context_text = "\n".join([
                f"{msg.get('role', 'user')}: {msg.get('content', '')}"
                for msg in recent_conversation
            ])
            
            return {
                "success": True,
                "context": context_text,
                "message_count": len(recent_conversation),
                "max_context_length": max_context_length,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "context": None,
                "message_count": 0,
                "max_context_length": max_context_length,
                "error": str(e)
            }
    
    def is_initialized(self) -> bool:
        """
        检查LangChain服务是否已初始化
        
        :return: 是否已初始化
        """
        return self.llm is not None
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取LangChain服务状态
        
        :return: 服务状态信息
        """
        return {
            "initialized": self.is_initialized(),
            "message": "LangChain服务已初始化" if self.is_initialized() else "LangChain服务未初始化，请配置DEEPSEEK_API_KEY"
        }


# 创建全局LangChain服务实例
langchain_service = LangChainService()
