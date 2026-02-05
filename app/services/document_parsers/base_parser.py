"""
    @project: aihub
    @Author: jiangkuanli
    @file: base_parser
    @date: 2026/2/2
    @desc: 文档解析基类
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import re


class BaseDocumentParser(ABC):
    """文档解析基类"""
    
    @abstractmethod
    def parse(self, file_path: str) -> Dict[str, Any]:
        """解析文档
        
        Args:
            file_path: 文件路径
            
        Returns:
            包含文档内容和元数据的字典
        """
        pass
    
    @abstractmethod
    def parse_from_bytes(self, file_content: bytes, file_type: str) -> Dict[str, Any]:
        """从字节数据解析文档
        
        Args:
            file_content: 文件字节数据
            file_type: 文件类型
            
        Returns:
            包含文档内容和元数据的字典
        """
        pass
    
    @abstractmethod
    def get_supported_extensions(self) -> List[str]:
        """获取支持的文件扩展名
        
        Returns:
            支持的文件扩展名列表
        """
        pass
    
    def clean_text(self, text: str) -> str:
        """清理文本，去除多余空格和特殊字符
        
        Args:
            text: 原始文本
            
        Returns:
            清理后的文本
        """
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        return text.strip()
    
    def extract_metadata(self, content: str) -> Dict[str, Any]:
        """提取文档元数据
        
        Args:
            content: 文档内容
            
        Returns:
            元数据字典
        """
        metadata = {
            'char_count': len(content),
            'line_count': len(content.split('\n')),
            'word_count': len(content.split())
        }
        return metadata
