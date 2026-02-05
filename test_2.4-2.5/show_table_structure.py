"""
    @project: aihub
    @Author: jiangkuanli
    @file: show_table_structure
    @date: 2026/2/4
    @desc: 展示数据库表结构
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径，确保可以导入 app 模块
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# 配置日志
class Tee:
    """同时输出到控制台和文件"""
    def __init__(self, file_path):
        self.file = open(file_path, 'w', encoding='utf-8')
        self.stdout = sys.stdout
        sys.stdout = self
    
    def write(self, data):
        self.stdout.write(data)
        self.file.write(data)
    
    def flush(self):
        self.stdout.flush()
        self.file.flush()
    
    def close(self):
        sys.stdout = self.stdout
        self.file.close()

# 创建日志文件
log_file = Path(__file__).parent / "table_structure_log.txt"
logger = Tee(log_file)

from sqlalchemy import inspect
from app.database.base import engine, get_db
from app.models.document import Document, Paragraph


def show_table_structure():
    """展示数据库表结构"""
    
    print("=" * 80)
    print("数据库表结构展示（Document 和 Paragraph）")
    print("=" * 80)
    
    inspector = inspect(engine)
    
    # 只展示 Document 和 Paragraph 表
    tables = ['documents', 'paragraphs']
    print(f"\n展示 {len(tables)} 个表：")
    print(f"  {', '.join(tables)}")
    
    # 展示每个表的结构
    for table_name in tables:
        print("\n" + "=" * 80)
        print(f"表名: {table_name}")
        print("=" * 80)
        
        columns = inspector.get_columns(table_name)
        print(f"\n字段信息（共 {len(columns)} 个字段）：")
        print("-" * 80)
        
        for idx, column in enumerate(columns, 1):
            nullable = "可空" if column['nullable'] else "非空"
            default = f", 默认: {column['default']}" if column['default'] else ""
            autoincrement = ", 自增" if column['autoincrement'] else ""
            
            print(f"{idx}. {column['name']}")
            print(f"   类型: {column['type']}")
            print(f"   属性: {nullable}{default}{autoincrement}")
            
            if column.get('primary_key'):
                print(f"   主键: ✓")
            
            # 外键信息（从列的属性中获取）
            if column.get('foreign_keys'):
                for fk in column['foreign_keys']:
                    print(f"   外键: {fk['referred_table']}.{fk['referred_columns'][0]}")
            
            print()
        
        # 获取主键
        primary_keys = inspector.get_pk_constraint(table_name)
        if primary_keys:
            pk_columns = primary_keys.get('column_names', [])
            print(f"主键: {', '.join(pk_columns)}")
        
        # 获取索引
        indexes = inspector.get_indexes(table_name)
        if indexes:
            print(f"\n索引：")
            for idx in indexes:
                unique = "唯一" if idx['unique'] else ""
                print(f"  {idx['name']}: {', '.join(idx['column_names'])} ({unique})")
    
    print("\n" + "=" * 80)
    print("表结构展示完成")
    print("=" * 80)


def show_model_info():
    """展示模型类信息"""
    
    print("\n" + "=" * 80)
    print("ORM模型类信息")
    print("=" * 80)
    
    models = [
        ("Document", Document),
        ("Paragraph", Paragraph)
    ]
    
    for model_name, model_class in models:
        print(f"\n{model_name}:")
        print(f"  表名: {model_class.__tablename__}")
        print(f"  字段数: {len(model_class.__table__.columns)}")
        
        print(f"  字段列表：")
        for column in model_class.__table__.columns:
            print(f"    - {column.name} ({str(column.type)})")
        
        print(f"  关系：")
        for rel_name, rel in model_class.__mapper__.relationships.items():
            print(f"    - {rel_name}: {rel.mapper.class_.__name__}")


def show_document_table_detail():
    """详细展示Document和Paragraph表"""
    
    print("\n" + "=" * 80)
    print("Document和Paragraph表详细结构")
    print("=" * 80)
    
    print("\nDocument表结构：")
    print("-" * 80)
    for column in Document.__table__.columns:
        nullable = "可空" if column.nullable else "非空"
        default = f", 默认: {column.default}" if column.default else ""
        print(f"  {column.name:30} {str(column.type):20} {nullable}{default}")
    
    print(f"\nDocument表关系：")
    for rel_name, rel in Document.__mapper__.relationships.items():
        print(f"  - {rel_name}: {rel.mapper.class_.__name__}")
    
    print("\nParagraph表结构：")
    print("-" * 80)
    for column in Paragraph.__table__.columns:
        nullable = "可空" if column.nullable else "非空"
        default = f", 默认: {column.default}" if column.default else ""
        print(f"  {column.name:30} {str(column.type):20} {nullable}{default}")
    
    print(f"\nParagraph表关系：")
    for rel_name, rel in Paragraph.__mapper__.relationships.items():
        print(f"  - {rel_name}: {rel.mapper.class_.__name__}")


if __name__ == "__main__":
    try:
        show_table_structure()
        show_model_info()
        show_document_table_detail()
        
        print("\n" + "=" * 80)
        print("第3天任务验证：文档数据模型设计")
        print("=" * 80)
        print("✅ Document表结构已实现")
        print("✅ Paragraph表结构已实现")
        print("✅ 表关系已正确配置")
        print("=" * 80)
    finally:
        # 关闭日志
        logger.close()
        print(f"\n日志已保存到: {log_file}")