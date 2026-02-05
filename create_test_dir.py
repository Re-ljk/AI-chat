"""
创建test_2.5-2.6目录并复制测试文件
"""

import os
import shutil
from pathlib import Path

# 创建目录
test_dir = Path("test_2.5-2.6")
test_dir.mkdir(exist_ok=True)
print(f"创建目录: {test_dir}")

# 复制测试文件
files_to_copy = [
    "test_minio_and_document_apis.py",
    "test_file.txt"
]

for file_name in files_to_copy:
    src_file = Path(file_name)
    dst_file = test_dir / file_name
    
    if src_file.exists():
        shutil.copy2(src_file, dst_file)
        print(f"复制文件: {src_file} -> {dst_file}")
    else:
        print(f"文件不存在: {src_file}")

# 验证结果
print("\n目录内容:")
for item in test_dir.iterdir():
    print(f"  - {item.name}")

print("\n操作完成！")
