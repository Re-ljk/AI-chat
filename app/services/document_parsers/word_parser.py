"""
    @project: aihub
    @Author: jiangkuanli
    @file: word_parser
    @date: 2026/2/2
    @desc: Word文档解析器
"""

from typing import Dict, Any
from .base_parser import BaseDocumentParser


class WordParser(BaseDocumentParser):
    """Word文档解析器"""
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """解析Word文档
        
        Args:
            file_path: Word文档路径
            
        Returns:
            包含文档内容和元数据的字典
        """
        try:
            from docx import Document
            
            doc = Document(file_path)
            content = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    content.append(paragraph.text)
            
            full_text = '\n'.join(content)
            cleaned_text = self.clean_text(full_text)
            
            metadata = self.extract_metadata(cleaned_text)
            metadata.update({
                'paragraph_count': len(doc.paragraphs),
                'table_count': len(doc.tables),
                'file_type': 'word'
            })
            
            return {
                'content': cleaned_text,
                'metadata': metadata,
                'success': True
            }
            
        except ImportError:
            return {
                'content': '',
                'metadata': {},
                'success': False,
                'error': 'python-docx库未安装，请运行: pip install python-docx'
            }
        except Exception as e:
            return {
                'content': '',
                'metadata': {},
                'success': False,
                'error': f'解析Word文档失败: {str(e)}'
            }
    
    def get_supported_extensions(self) -> list:
        """获取支持的文件扩展名"""
        return ['.docx', '.doc']
