"""
    @project: aihub
    @Author: jiangkuanli
    @file: pdf_parser
    @date: 2026/2/3
    @desc: PDF文档解析器（支持OCR）
"""

from typing import Dict, Any, List
import base64
import os
import tempfile
from .base_parser import BaseDocumentParser


class PDFParser(BaseDocumentParser):
    """PDF文档解析器（支持OCR）"""
    
    def __init__(self):
        """初始化PDF解析器"""
        self.use_ocr = False
        self.ocr_engine = None
    
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
            
            # 检测PDF是否为扫描版本
            is_scanned = self._detect_scanned_pdf(reader)
            
            if is_scanned:
                print("检测到扫描版PDF，使用OCR提取文字")
                return self._parse_with_ocr(file_path, reader)
            else:
                print("检测到普通PDF，使用pypdf提取文字")
                return self._parse_with_pypdf(reader)
                
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
    
    def _detect_scanned_pdf(self, reader) -> bool:
        """检测PDF是否为扫描版本
        
        Args:
            reader: PdfReader对象
            
        Returns:
            True表示扫描版PDF，False表示普通PDF
        """
        try:
            # 方法1：检查前几页是否包含可提取的文本
            check_pages = min(3, len(reader.pages))
            total_text_length = 0
            
            for i in range(check_pages):
                try:
                    page_text = reader.pages[i].extract_text()
                    if page_text:
                        total_text_length += len(page_text.strip())
                except:
                    pass
            
            # 如果前几页平均每页文本少于50个字符，可能是扫描版
            if total_text_length < 50 * check_pages:
                return True
            
            # 方法2：检查是否包含图片XObject
            for page in reader.pages[:check_pages]:
                try:
                    if '/Resources' in page and '/XObject' in page['/Resources']:
                        x_objects = page['/Resources']['/XObject']
                        if len(x_objects) > 0:
                            # 有图片对象，可能是扫描版
                            return True
                except:
                    pass
            
            return False
            
        except Exception as e:
            print(f"检测PDF类型时出错: {str(e)}")
            return False
    
    def _parse_with_pypdf(self, reader) -> Dict[str, Any]:
        """使用pypdf解析普通PDF
        
        Args:
            reader: PdfReader对象
            
        Returns:
            解析结果
        """
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
            'is_encrypted': reader.is_encrypted,
            'is_scanned': False,
            'extraction_method': 'pypdf'
        })
        
        return {
            'content': cleaned_text,
            'metadata': metadata,
            'images': images,
            'success': True
        }
    
    def _parse_with_ocr(self, file_path: str, reader) -> Dict[str, Any]:
        """使用OCR解析扫描版PDF
        
        Args:
            file_path: PDF文件路径
            reader: PdfReader对象
            
        Returns:
            解析结果
        """
        try:
            from pdf2image import convert_from_path
            from paddleocr import PaddleOCR
            
            # 初始化OCR引擎
            if self.ocr_engine is None:
                self.ocr_engine = PaddleOCR(use_angle_cls=True, lang='ch')
            
            # 将PDF转换为图片
            images = convert_from_path(
                file_path,
                dpi=200,
                fmt='jpeg',
                thread_count=4
            )
            
            content = []
            extracted_images = []
            
            for i, image in enumerate(images):
                try:
                    # 使用OCR识别文字
                    result = self.ocr_engine.ocr(image, cls=True)
                    
                    if result and result[0]:
                        # 提取识别的文字
                        page_text = '\n'.join([line[1][0] for line in result[0] if line[1]])
                        if page_text.strip():
                            content.append(f"--- 第 {i + 1} 页 ---\n{page_text}")
                        
                        # 保存图片信息
                        image_bytes = self._image_to_bytes(image)
                        if image_bytes:
                            image_info = {
                                'index': len(extracted_images),
                                'page': i + 1,
                                'size': len(image_bytes),
                                'data': base64.b64encode(image_bytes).decode('utf-8')
                            }
                            extracted_images.append(image_info)
                except Exception as e:
                    print(f"OCR识别第 {i + 1} 页时出错: {str(e)}")
                    continue
            
            full_text = '\n\n'.join(content)
            cleaned_text = self.clean_text(full_text)
            
            # 提取嵌入的图片
            embedded_images = []
            self._extract_images(reader, embedded_images)
            
            # 合并OCR提取的图片和嵌入的图片
            all_images = extracted_images + embedded_images
            
            metadata = self.extract_metadata(cleaned_text)
            metadata.update({
                'page_count': len(images),
                'image_count': len(all_images),
                'has_images': len(all_images) > 0,
                'file_type': 'pdf',
                'is_encrypted': reader.is_encrypted,
                'is_scanned': True,
                'extraction_method': 'paddleocr'
            })
            
            return {
                'content': cleaned_text,
                'metadata': metadata,
                'images': all_images,
                'success': True
            }
            
        except ImportError as e:
            return {
                'content': '',
                'metadata': {},
                'images': [],
                'success': False,
                'error': f'OCR库未安装，请运行: pip install pdf2image paddlepaddle paddleocr Pillow'
            }
        except Exception as e:
            return {
                'content': '',
                'metadata': {},
                'images': [],
                'success': False,
                'error': f'OCR解析PDF失败: {str(e)}'
            }
    
    def _image_to_bytes(self, image) -> bytes:
        """将PIL图像转换为bytes
        
        Args:
            image: PIL图像对象
            
        Returns:
            图像的bytes数据
        """
        try:
            from io import BytesIO
            buffer = BytesIO()
            image.save(buffer, format='JPEG')
            return buffer.getvalue()
        except Exception as e:
            print(f"转换图像为bytes时出错: {str(e)}")
            return None
    
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
                    if '/Resources' in page and '/XObject' in page['/Resources']:
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
    
    def parse_from_bytes(self, file_content: bytes, file_type: str) -> Dict[str, Any]:
        """从字节数据解析PDF文档
        
        Args:
            file_content: 文件字节数据
            file_type: 文件类型
            
        Returns:
            包含文档内容和元数据的字典
        """
        try:
            import pypdf
            
            # 创建临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
            
            try:
                reader = pypdf.PdfReader(temp_file_path)
                
                # 检测PDF是否为扫描版本
                is_scanned = self._detect_scanned_pdf(reader)
                
                if is_scanned:
                    print("检测到扫描版PDF，使用OCR提取文字")
                    result = self._parse_with_ocr(temp_file_path, reader)
                else:
                    print("检测到普通PDF，使用pypdf提取文字")
                    result = self._parse_with_pypdf(reader)
                
                return result
            finally:
                # 删除临时文件
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                
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
