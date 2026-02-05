# test_2.5-2.6 测试说明

## 目录结构

```
test_2.5-2.6/
├── test_minio_and_document_apis.py  # MinIO和文档API测试脚本
├── test_file.txt                    # 测试用文本文件
├── test_log.txt                     # 测试输出日志（自动生成）
└── README.md                        # 本说明文件
```

## 文件说明

### 1. test_minio_and_document_apis.py
**功能**：完整的MinIO对象存储和文档API测试脚本

**测试内容**：
- ✅ 用户登录认证
- ✅ MinIO服务测试（上传、下载、URL生成、删除）
- ✅ 文档上传测试
- ✅ 文档列表查询测试（含分页、状态筛选、文件类型筛选、搜索）
- ✅ 文档详情查询测试
- ✅ 文档下载测试
- ✅ 文档段落查询测试（含分页、搜索）
- ✅ 文档删除测试

**特点**：
- 自动记录测试日志到 `test_log.txt`
- 支持命令行参数配置
- 详细的测试结果输出

### 2. test_file.txt
**功能**：测试用的文本文件

**内容**：用于验证文档上传、解析、分段和下载功能的测试文本

### 3. test_log.txt
**功能**：测试输出日志文件

**生成方式**：运行测试脚本时自动生成，记录完整的测试过程和结果

## 运行测试

### 前置条件
1. 后端服务已启动（http://localhost:8000）
2. MinIO服务已运行（API端口：9005）
3. 存在有效的用户账户（默认：jiangkuanli/123456）

### 运行步骤

1. **进入测试目录**
   ```bash
   cd test_2.5-2.6
   ```

2. **运行测试脚本**
   ```bash
   # 使用默认测试文件
   python test_minio_and_document_apis.py --file "test_file.txt"
   
   # 或指定其他测试文件
   python test_minio_and_document_apis.py --file "path/to/other/file.txt"
   
   ```

## 运行示例

```bash
# 运行完整测试
python test_minio_and_document_apis.py --file "test_file.txt"

# 预期输出
============================================================
  MinIO和文档API接口测试
============================================================

============================================================
  用户登录
============================================================

✓ 通过 - 用户登录
  用户: jiangkuanli

============================================================
  测试MinIO服务
============================================================

DeepSeek LLM初始化成功
✓ 通过 - MinIO上传文件
  对象名: test_file.txt
✓ 通过 - MinIO下载文件
  数据匹配
✓ 通过 - MinIO生成URL
  URL: http://localhost:9005/documents/test_file.txt?X-Am...
✓ 通过 - MinIO删除文件

# ... 更多测试输出 ...

日志已保存到: test_2.5-2.6\test_log.txt
```
