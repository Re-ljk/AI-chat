"""
    @project: aihub
    @Author: jiangkuanli
    @file: unstructured_parser
    @date: 2026/2/3
    @desc: Unstructured集成解析器
"""

import os
from io import BytesIO
from typing import Dict, Any, List
from .base_parser import BaseDocumentParser

# 设置NLTK数据目录到项目目录，避免权限问题
NLTK_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'nltk_data')
os.makedirs(NLTK_DATA_DIR, exist_ok=True)
os.environ['NLTK_DATA'] = NLTK_DATA_DIR


class UnstructuredParser(BaseDocumentParser):
    """Unstructured集成解析器"""
    
    def __init__(self):
        """初始化Unstructured解析器"""
        self.supported_formats = [
            '.pdf', '.docx', '.doc', '.pptx', '.ppt',
            '.xlsx', '.xls', '.csv', '.txt', '.md', '.html'
        ]
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """使用Unstructured解析文档
        
        Args:
            file_path: 文档路径
            
        Returns:
            包含文档内容和元数据的字典
        """
        try:
            from unstructured.partition.auto import partition
            
            elements = partition(filename=file_path)
            
            content = []
            metadata = {
                'element_count': len(elements),
                'file_type': 'unstructured'
            }
            
            for element in elements:
                element_text = str(element).strip()
                if element_text:
                    content.append(element_text)
            
            full_text = '\n\n'.join(content)
            cleaned_text = self.clean_text(full_text)
            
            element_types = {}
            for element in elements:
                element_type = type(element).__name__
                element_types[element_type] = element_types.get(element_type, 0) + 1
            
            metadata.update({
                'element_types': element_types,
                'unique_element_types': len(element_types)
            })
            
            return {
                'content': cleaned_text,
                'metadata': metadata,
                'elements': [{'type': type(e).__name__, 'text': str(e)[:100]} for e in elements[:10]],
                'success': True
            }
            
        except ImportError:
            return {
                'content': '',
                'metadata': {},
                'elements': [],
                'success': False,
                'error': 'unstructured库未安装，请运行: pip install unstructured'
            }
        except Exception as e:
            return {
                'content': '',
                'metadata': {},
                'elements': [],
                'success': False,
                'error': f'Unstructured解析失败: {str(e)}'
            }
    
    def parse_from_bytes(self, file_content: bytes, file_type: str) -> Dict[str, Any]:
        """从字节数据解析文档
        
        Args:
            file_content: 文件字节数据
            file_type: 文件类型
            
        Returns:
            包含文档内容和元数据的字典
        """
        try:
            # 对于文本文件，直接处理
            if file_type.lower() in ['txt', 'text']:
                try:
                    text_content = file_content.decode('utf-8')
                except UnicodeDecodeError:
                    # 尝试其他编码
                    try:
                        text_content = file_content.decode('gbk')
                    except:
                        text_content = file_content.decode('latin1')
                
                cleaned_text = self.clean_text(text_content)
                metadata = self.extract_metadata(cleaned_text)
                metadata.update({
                    'file_type': 'text',
                    'parsing_method': 'direct_text'
                })
                
                return {
                    'content': cleaned_text,
                    'metadata': metadata,
                    'elements': [{'type': 'Text', 'text': cleaned_text[:100]}],
                    'success': True
                }
            
            # 对于其他文件类型，使用unstructured
            from unstructured.partition.auto import partition
            
            content_stream = BytesIO(file_content)
            
            elements = partition(file=content_stream)
            
            content = []
            metadata = {
                'element_count': len(elements),
                'file_type': 'unstructured'
            }
            
            for element in elements:
                element_text = str(element).strip()
                if element_text:
                    content.append(element_text)
            
            full_text = '\n\n'.join(content)
            cleaned_text = self.clean_text(full_text)
            
            element_types = {}
            for element in elements:
                element_type = type(element).__name__
                element_types[element_type] = element_types.get(element_type, 0) + 1
            
            metadata.update({
                'element_types': element_types,
                'unique_element_types': len(element_types)
            })
            
            return {
                'content': cleaned_text,
                'metadata': metadata,
                'elements': [{'type': type(e).__name__, 'text': str(e)[:100]} for e in elements[:10]],
                'success': True
            }
            
        except ImportError:
            return {
                'content': '',
                'metadata': {},
                'elements': [],
                'success': False,
                'error': 'unstructured库未安装，请运行: pip install unstructured'
            }
        except Exception as e:
            return {
                'content': '',
                'metadata': {},
                'elements': [],
                'success': False,
                'error': f'Unstructured解析失败: {str(e)}'
            }
    
    def get_supported_extensions(self) -> list:
        """获取支持的文件扩展名"""
        return self.supported_formats
