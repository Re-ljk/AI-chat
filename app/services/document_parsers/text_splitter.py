"""
    @project: aihub
    @Author: jiangkuanli
    @file: text_splitter
    @date: 2026/2/2
    @desc: 文本分段器
"""

from typing import List, Dict, Any
from abc import ABC, abstractmethod
import re


class BaseTextSplitter(ABC):
    """文本分段基类"""
    
    @abstractmethod
    def split_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """分段文本
        
        Args:
            text: 待分段的文本
            metadata: 文档元数据
            
        Returns:
            分段后的文本列表，每个元素包含内容和元数据
        """
        pass


class RecursiveCharacterSplitter(BaseTextSplitter):
    """递归字符分段器"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        初始化递归字符分段器
        
        Args:
            chunk_size: 每段的最大字符数
            chunk_overlap: 段落之间的重叠字符数
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """使用递归字符分段
        
        Args:
            text: 待分段的文本
            metadata: 文档元数据
            
        Returns:
            分段后的文本列表
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]
            
            chunk_metadata = metadata.copy() if metadata else {}
            chunk_metadata.update({
                'chunk_index': len(chunks),
                'start_char': start,
                'end_char': min(end, text_length),
                'char_count': len(chunk)
            })
            
            chunks.append({
                'content': chunk,
                'metadata': chunk_metadata
            })
            
            start = end - self.chunk_overlap
        
        return chunks


class MarkdownHeaderSplitter(BaseTextSplitter):
    """Markdown标题分段器"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        初始化Markdown标题分段器
        
        Args:
            chunk_size: 每段的最大字符数
            chunk_overlap: 段落之间的重叠字符数
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.header_pattern = re.compile(r'^(#{1,6}\s+.+)$', re.MULTILINE)
    
    def split_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """使用Markdown标题进行分段
        
        Args:
            text: 待分段的Markdown文本
            metadata: 文档元数据
            
        Returns:
            分段后的文本列表
        """
        lines = text.split('\n')
        chunks = []
        current_chunk = []
        current_size = 0
        
        for line in lines:
            line_size = len(line)
            
            if current_size + line_size > self.chunk_size:
                if current_chunk:
                    chunk_text = '\n'.join(current_chunk)
                    chunk_metadata = metadata.copy() if metadata else {}
                    chunk_metadata.update({
                        'chunk_index': len(chunks),
                        'char_count': len(chunk_text),
                        'split_method': 'markdown_header'
                    })
                    chunks.append({
                        'content': chunk_text,
                        'metadata': chunk_metadata
                    })
                
                current_chunk = [line]
                current_size = line_size
            else:
                current_chunk.append(line)
                current_size += line_size
        
        if current_chunk:
            chunk_text = '\n'.join(current_chunk)
            chunk_metadata = metadata.copy() if metadata else {}
            chunk_metadata.update({
                'chunk_index': len(chunks),
                'char_count': len(chunk_text),
                'split_method': 'markdown_header'
            })
            chunks.append({
                'content': chunk_text,
                'metadata': chunk_metadata
            })
        
        return chunks


class CodeSyntaxSplitter(BaseTextSplitter):
    """代码语法分段器"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        初始化代码语法分段器
        
        Args:
            chunk_size: 每段的最大字符数
            chunk_overlap: 段落之间的重叠字符数
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.code_block_pattern = re.compile(r'```[\s\S]*?\n([\s\S]*?)\n```', re.MULTILINE)
    
    def split_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """使用代码语法进行分段
        
        Args:
            text: 待分段的文本
            metadata: 文档元数据
            
        Returns:
            分段后的文本列表
        """
        chunks = []
        code_blocks = self.code_block_pattern.split(text)
        
        for i, code_block in enumerate(code_blocks):
            if i % 2 == 0:
                if len(code_block) > self.chunk_size:
                    sub_chunks = self._split_by_size(code_block, self.chunk_size)
                    for sub_chunk in sub_chunks:
                        chunk_metadata = metadata.copy() if metadata else {}
                        chunk_metadata.update({
                            'chunk_index': len(chunks),
                            'char_count': len(sub_chunk),
                            'split_method': 'code_syntax',
                            'is_code': True
                        })
                        chunks.append({
                            'content': sub_chunk,
                            'metadata': chunk_metadata
                        })
                else:
                    chunk_metadata = metadata.copy() if metadata else {}
                    chunk_metadata.update({
                        'chunk_index': len(chunks),
                        'char_count': len(code_block),
                        'split_method': 'code_syntax',
                        'is_code': True
                    })
                    chunks.append({
                        'content': code_block,
                        'metadata': chunk_metadata
                    })
        
        return chunks
    
    def _split_by_size(self, text: str, size: int) -> List[str]:
        """按大小分割文本"""
        chunks = []
        for i in range(0, len(text), size):
            chunks.append(text[i:i + size])
        return chunks
