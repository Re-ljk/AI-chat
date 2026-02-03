"""
    @project: aihub
    @Author: jiangkuanli
    @file: test_image_extraction
    @date: 2026/2/2
    @desc: 测试文档中的图片提取功能
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.document_parser_service import document_parser_service


def test_word_image_extraction():
    """测试Word文档图片提取"""
    print("=" * 60)
    print("测试Word文档图片提取")
    print("=" * 60)
    
    word_file = "test_documents/sample.docx"
    
    if not os.path.exists(word_file):
        print(f"测试文件不存在: {word_file}")
        print("请运行: python create_test_documents.py")
        return
    
    result = document_parser_service.parse_document(word_file)
    
    if result['success']:
        print(f"✓ 解析成功")
        print(f"  - 字符数: {result['metadata'].get('char_count', 0)}")
        print(f"  - 行数: {result['metadata'].get('line_count', 0)}")
        print(f"  - 词数: {result['metadata'].get('word_count', 0)}")
        print(f"  - 段落数: {result['metadata'].get('paragraph_count', 0)}")
        print(f"  - 表格数: {result['metadata'].get('table_count', 0)}")
        print(f"  - 图片数: {result['metadata'].get('image_count', 0)}")
        print(f"  - 是否包含图片: {result['metadata'].get('has_images', False)}")
        
        images = result.get('images', [])
        if images:
            print(f"\n  - 图片详情:")
            for img in images:
                print(f"    图片 {img['index']}:")
                print(f"      - 扩展名: {img['extension']}")
                print(f"      - 大小: {img['size']} bytes")
                print(f"      - Base64长度: {len(img['data'])} chars")
        else:
            print(f"\n  - 文档中没有图片")
    else:
        print(f"✗ 解析失败: {result.get('error', '未知错误')}")
    
    print()


def test_excel_image_extraction():
    """测试Excel文档图片提取"""
    print("=" * 60)
    print("测试Excel文档图片提取")
    print("=" * 60)
    
    excel_file = "test_documents/sample.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"测试文件不存在: {excel_file}")
        print("请运行: python create_test_documents.py")
        return
    
    result = document_parser_service.parse_document(excel_file)
    
    if result['success']:
        print(f"✓ 解析成功")
        print(f"  - 字符数: {result['metadata'].get('char_count', 0)}")
        print(f"  - 行数: {result['metadata'].get('line_count', 0)}")
        print(f"  - 词数: {result['metadata'].get('word_count', 0)}")
        print(f"  - 工作表数: {result['metadata'].get('sheet_count', 0)}")
        print(f"  - 列数: {result['metadata'].get('column_count', 0)}")
        print(f"  - 行数: {result['metadata'].get('row_count', 0)}")
        print(f"  - 图片数: {result['metadata'].get('image_count', 0)}")
        print(f"  - 是否包含图片: {result['metadata'].get('has_images', False)}")
        
        images = result.get('images', [])
        if images:
            print(f"\n  - 图片详情:")
            for img in images:
                print(f"    图片 {img['index']}:")
                print(f"      - 工作表: {img.get('sheet', 'N/A')}")
                print(f"      - 扩展名: {img['extension']}")
                print(f"      - 大小: {img['size']} bytes")
                print(f"      - Base64长度: {len(img['data'])} chars")
        else:
            print(f"\n  - 文档中没有图片")
    else:
        print(f"✗ 解析失败: {result.get('error', '未知错误')}")
    
    print()


def test_save_image():
    """测试保存图片到文件"""
    print("=" * 60)
    print("测试保存图片到文件")
    print("=" * 60)
    
    word_file = "test_documents/sample.docx"
    
    if not os.path.exists(word_file):
        print(f"测试文件不存在: {word_file}")
        return
    
    result = document_parser_service.parse_document(word_file)
    
    if result['success']:
        images = result.get('images', [])
        
        if images:
            import base64
            
            output_dir = "test_documents/extracted_images"
            os.makedirs(output_dir, exist_ok=True)
            
            for img in images:
                try:
                    image_data = base64.b64decode(img['data'])
                    output_path = os.path.join(output_dir, f"image_{img['index']}.{img['extension']}")
                    
                    with open(output_path, 'wb') as f:
                        f.write(image_data)
                    
                    print(f"✓ 已保存图片: {output_path}")
                except Exception as e:
                    print(f"✗ 保存图片失败: {str(e)}")
        else:
            print("文档中没有图片")
    else:
        print(f"解析失败: {result.get('error', '未知错误')}")
    
    print()


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("文档图片提取功能测试")
    print("=" * 60 + "\n")
    
    test_word_image_extraction()
    test_excel_image_extraction()
    test_save_image()
    
    print("测试完成！")
    print("\n注意：")
    print("- Word和Excel文档解析需要实际的测试文件")
    print("- 图片提取功能已实现，可以提取文档中的图片")
    print("- 图片以Base64编码格式返回")
    print("- 可以将Base64解码后保存为图片文件\n")


if __name__ == "__main__":
    main()
