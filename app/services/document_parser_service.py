"""
    @project: aihub
    @Author: jiangkuanli
    @file: document_parser_service
    @date: 2026/2/2
    @desc: 文档解析服务
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import os

from .document_parsers.base_parser import BaseDocumentParser
from .document_parsers.word_parser import WordParser
from .document_parsers.excel_parser import ExcelParser
from .document_parsers.pdf_parser import PDFParser
from .document_parsers.unstructured_parser import UnstructuredParser
from .document_parsers.text_splitter import (
    RecursiveCharacterSplitter,
    MarkdownHeaderSplitter,
    CodeSyntaxSplitter,
    BaseTextSplitter
)


class DocumentParserService:
    """文档解析服务"""
    
    def __init__(self):
        """初始化文档解析服务"""
        self.parsers: Dict[str, BaseDocumentParser] = {
            'word': WordParser(),
            'excel': ExcelParser(),
            'pdf': PDFParser(),
            'unstructured': UnstructuredParser()
        }
        
        self.splitters: Dict[str, BaseTextSplitter] = {
            'recursive_char': RecursiveCharacterSplitter(),
            'markdown_header': MarkdownHeaderSplitter(),
            'code_syntax': CodeSyntaxSplitter()
        }
    
    def get_parser(self, file_path: str) -> Optional[BaseDocumentParser]:
        """根据文件扩展名获取对应的解析器
        
        Args:
            file_path: 文件路径
            
        Returns:
            文档解析器实例，如果不支持则返回None
        """
        file_extension = Path(file_path).suffix.lower()
        
        for parser_name, parser in self.parsers.items():
            if file_extension in parser.get_supported_extensions():
                return parser
        
        return None
    
    def parse_document(self, file_path: str) -> Dict[str, Any]:
        """解析文档
        
        Args:
            file_path: 文件路径
            
        Returns:
            包含解析结果、分段结果的字典
        """
        parser = self.get_parser(file_path)
        
        if not parser:
            return {
                'success': False,
                'error': f'不支持的文件类型: {Path(file_path).suffix}',
                'content': '',
                'metadata': {},
                'chunks': []
            }
        
        parse_result = parser.parse(file_path)
        
        if not parse_result.get('success', False):
            return {
                'success': False,
                'error': parse_result.get('error', '解析失败'),
                'content': '',
                'metadata': {},
                'chunks': []
            }
        
        return {
            'success': True,
            'error': None,
            'content': parse_result.get('content', ''),
            'metadata': parse_result.get('metadata', {}),
            'chunks': []
        }
    
    def split_document(
        self,
        content: str,
        metadata: Dict[str, Any],
        split_method: str = 'recursive_char',
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> List[Dict[str, Any]]:
        """分段文档
        
        Args:
            content: 文档内容
            metadata: 文档元数据
            split_method: 分段方法（recursive_char/markdown_header/code_syntax）
            chunk_size: 每段最大字符数
            chunk_overlap: 段落重叠字符数
            
        Returns:
            分段后的文本列表
        """
        splitter = self.splitters.get(split_method)
        
        if not splitter:
            return []
        
        return splitter.split_text(content, metadata)
    
    def parse_and_split(
        self,
        file_path: str,
        split_method: str = 'recursive_char',
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> Dict[str, Any]:
        """解析文档并分段
        
        Args:
            file_path: 文件路径
            split_method: 分段方法
            chunk_size: 每段最大字符数
            chunk_overlap: 段落重叠字符数
            
        Returns:
            包含解析结果和分段结果的字典
        """
        parse_result = self.parse_document(file_path)
        
        if not parse_result.get('success', False):
            return parse_result
        
        content = parse_result.get('content', '')
        metadata = parse_result.get('metadata', {})
        
        chunks = self.split_document(
            content,
            metadata,
            split_method,
            chunk_size,
            chunk_overlap
        )
        
        return {
            'success': True,
            'error': None,
            'content': content,
            'metadata': metadata,
            'chunks': chunks
        }
    
    def get_supported_extensions(self) -> List[str]:
        """获取所有支持的文件扩展名"""
        extensions = []
        for parser in self.parsers.values():
            extensions.extend(parser.get_supported_extensions())
        return list(set(extensions))
    
    def get_available_parsers(self) -> List[str]:
        """获取所有可用的解析器名称"""
        return list(self.parsers.keys())
    
    def get_available_splitters(self) -> List[str]:
        """获取所有可用的分段器名称"""
        return list(self.splitters.keys())


document_parser_service = DocumentParserService()
