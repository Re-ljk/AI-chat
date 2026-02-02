"""
    @project: aihub
    @Author: jiangkuanli
    @file: excel_parser
    @date: 2026/2/2
    @desc: Excel文档解析器
"""

from typing import Dict, Any, List
from .base_parser import BaseDocumentParser


class ExcelParser(BaseDocumentParser):
    """Excel文档解析器"""
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """解析Excel文档
        
        Args:
            file_path: Excel文档路径
            
        Returns:
            包含文档内容和元数据的字典
        """
        try:
            import pandas as pd
            
            df = pd.read_excel(file_path)
            content = []
            
            for column in df.columns:
                column_data = df[column].dropna().astype(str).tolist()
                content.append(f"{column}:\n" + "\n".join(column_data))
                content.append("\n")
            
            full_text = '\n'.join(content)
            cleaned_text = self.clean_text(full_text)
            
            metadata = self.extract_metadata(cleaned_text)
            metadata.update({
                'sheet_count': len(df.sheet_names),
                'column_count': len(df.columns),
                'row_count': len(df),
                'file_type': 'excel'
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
                'error': 'pandas或openpyxl库未安装，请运行: pip install pandas openpyxl'
            }
        except Exception as e:
            return {
                'content': '',
                'metadata': {},
                'success': False,
                'error': f'解析Excel文档失败: {str(e)}'
            }
    
    def get_supported_extensions(self) -> list:
        """获取支持的文件扩展名"""
        return ['.xlsx', '.xls', '.csv']
