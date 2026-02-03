"""
    @project: aihub
    @Author: jiangkuanli
    @file: pdf_parser
    @date: 2026/2/3
    @desc: PDF文档解析器
"""

from typing import Dict, Any, List
import base64
from .base_parser import BaseDocumentParser


class PDFParser(BaseDocumentParser):
    """PDF文档解析器"""
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """解析PDF文档
        
        Args:
            file_path: PDF文档路径
            
        Returns:
            包含文档内容和元数据的字典
        """
        try:
            import pypdf
            
            reader = pypdf.PdfReader(file_path)
            content = []
            images = []
            
            for page_num, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        content.append(f"--- 第 {page_num + 1} 页 ---\n{page_text}")
                except Exception as e:
                    print(f"提取第 {page_num + 1} 页文本时出错: {str(e)}")
                    continue
            
            full_text = '\n\n'.join(content)
            cleaned_text = self.clean_text(full_text)
            
            image_count = self._extract_images(reader, images)
            
            metadata = self.extract_metadata(cleaned_text)
            metadata.update({
                'page_count': len(reader.pages),
                'image_count': image_count,
                'has_images': image_count > 0,
                'file_type': 'pdf',
                'is_encrypted': reader.is_encrypted
            })
            
            return {
                'content': cleaned_text,
                'metadata': metadata,
                'images': images,
                'success': True
            }
            
        except ImportError:
            return {
                'content': '',
                'metadata': {},
                'images': [],
                'success': False,
                'error': 'pypdf库未安装，请运行: pip install pypdf'
            }
        except Exception as e:
            return {
                'content': '',
                'metadata': {},
                'images': [],
                'success': False,
                'error': f'解析PDF文档失败: {str(e)}'
            }
    
    def _extract_images(self, reader, images: List[Dict[str, Any]]) -> int:
        """提取PDF文档中的图片
        
        Args:
            reader: PdfReader对象
            images: 图片列表
            
        Returns:
            图片数量
        """
        try:
            image_count = 0
            
            for page_num, page in enumerate(reader.pages):
                try:
                    if '/XObject' in page['/Resources']:
                        x_objects = page['/Resources']['/XObject'].get_object()
                        
                        for obj_name in x_objects:
                            if x_objects[obj_name]['/Subtype'] == '/Image':
                                try:
                                    image_data = x_objects[obj_name]._data
                                    if image_data:
                                        image_info = {
                                            'index': image_count,
                                            'page': page_num + 1,
                                            'size': len(image_data),
                                            'data': base64.b64encode(image_data).decode('utf-8')
                                        }
                                        images.append(image_info)
                                        image_count += 1
                                except Exception as e:
                                    print(f"提取第 {page_num + 1} 页图片 {image_count} 时出错: {str(e)}")
                                    continue
                except Exception as e:
                    print(f"处理第 {page_num + 1} 页资源时出错: {str(e)}")
                    continue
            
            return image_count
        except Exception as e:
            print(f"提取PDF图片时出错: {str(e)}")
            return 0
    
    def get_supported_extensions(self) -> list:
        """获取支持的文件扩展名"""
        return ['.pdf']
