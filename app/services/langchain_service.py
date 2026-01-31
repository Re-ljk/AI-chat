"""
    @project: aihub
    @Author: jiangkuanli
    @file: langchain_service
    @date: 2026/1/29
    @desc: LangChain集成服务，实现对话历史学习
"""

from typing import List, Dict, Any
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder

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
        self.conversation_memory = None
        self.conversation_chain = None
        
        # 如果配置了OpenAI API密钥，则初始化LLM
        if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
            self._initialize_openai()
    
    def _initialize_openai(self):
        """
        初始化OpenAI LLM
        """
        try:
            self.llm = ChatOpenAI(
                openai_api_key=settings.OPENAI_API_KEY,
                model="gpt-3.5-turbo",
                temperature=0.7
            )
            print("OpenAI LLM初始化成功")
        except Exception as e:
            print(f"OpenAI LLM初始化失败: {e}")
    
    def create_conversation_memory(self, conversation_history: List[Dict[str, Any]]) -> ConversationBufferMemory:
        """
        从对话历史创建LangChain记忆对象
        
        :param conversation_history: 对话历史列表
        :return: LangChain记忆对象
        """
        memory = ConversationBufferMemory()
        
        # 将对话历史转换为LangChain格式
        for message in conversation_history:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if role == "user":
                memory.chat_memory.add_user_message(content)
            elif role == "assistant":
                memory.chat_memory.add_ai_message(content)
        
        return memory
    
    def create_conversation_chain(self, memory: ConversationBufferMemory = None) -> ConversationChain:
        """
        创建对话链
        
        :param memory: LangChain记忆对象
        :return: 对话链
        """
        if self.llm is None:
            raise ValueError("LLM未初始化，请检查API密钥配置")
        
        if memory is None:
            memory = ConversationBufferMemory()
        
        # 创建对话提示模板
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "你是一个有用的AI助手。请根据对话历史提供有帮助的回答。"
            ),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # 创建对话链
        chain = ConversationChain(
            llm=self.llm,
            memory=memory,
            prompt=prompt,
            verbose=True
        )
        
        return chain
    
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
            # 创建对话记忆
            if conversation_history:
                memory = self.create_conversation_memory(conversation_history)
            else:
                memory = ConversationBufferMemory()
            
            # 创建对话链
            chain = self.create_conversation_chain(memory)
            
            # 生成回复
            response = await chain.apredict(input=user_message)
            
            return {
                "success": True,
                "response": response,
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
    
    def summarize_conversation(self, conversation_history: List[Dict[str, Any]]) -> str:
        """
        总结对话历史
        
        :param conversation_history: 对话历史
        :return: 对话总结
        """
        if not conversation_history:
            return "无对话历史"
        
        try:
            # 将对话历史转换为文本
            conversation_text = "\n".join([
                f"{msg.get('role', 'user')}: {msg.get('content', '')}"
                for msg in conversation_history
            ])
            
            # 使用LLM生成总结
            if self.llm is None:
                return "LLM未初始化，无法生成总结"
            
            summary_prompt = f"""
            请总结以下对话，提取关键信息：
            
            {conversation_text}
            
            请提供简洁的总结，包括：
            1. 对话主题
            2. 主要讨论点
            3. 用户需求
            """
            
            summary = self.llm.predict(summary_prompt)
            
            return summary
            
        except Exception as e:
            return f"总结生成失败: {str(e)}"
    
    def get_context_from_history(
        self,
        conversation_history: List[Dict[str, Any]],
        max_context_length: int = 10
    ) -> str:
        """
        从对话历史中提取上下文
        
        :param conversation_history: 对话历史
        :param max_context_length: 最大上下文长度
        :return: 上下文文本
        """
        if not conversation_history:
            return ""
        
        # 获取最近的N条消息作为上下文
        recent_messages = conversation_history[-max_context_length:]
        
        context_parts = []
        for msg in recent_messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            context_parts.append(f"{role}: {content}")
        
        return "\n".join(context_parts)
    
    def is_initialized(self) -> bool:
        """
        检查服务是否已初始化
        
        :return: 是否已初始化
        """
        return self.llm is not None


# 全局LangChain服务实例
langchain_service = LangChainService()
