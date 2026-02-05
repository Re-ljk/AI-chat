# 测试脚本说明文档

## 目录结构
```
test_2.4-2.5/
├── show_table_structure.py     # 数据库表结构展示脚本
├── test_document_api.py        # 文档API测试脚本
├── table_structure_log.txt     # 表结构日志文件
├── document_api_test_log.txt   # API测试日志文件
└── README.md                   # 本说明文档
```

## 脚本功能说明

### 1. show_table_structure.py
**功能**：展示数据库表结构和模型信息

**主要功能**：
- 显示 `Document` 和 `Paragraph` 表的完整结构
- 展示 SQLAlchemy 模型定义和字段信息
- 验证表关系配置
- 生成详细的日志记录

**运行结果**：
- 控制台输出：实时显示表结构信息
- 日志文件：`table_structure_log.txt` 保存完整输出

### 2. test_document_api.py
**功能**：测试文档管理API接口

**测试步骤**：
1. 登录获取访问令牌
2. 上传测试文档
3. 获取文档列表
4. 获取文档详情
5. 获取文档段落
6. 更新文档状态
7. 删除文档
8. 验证文档删除

**运行结果**：
- 控制台输出：实时显示测试进度和结果
- 日志文件：`document_api_test_log.txt` 保存完整测试过程

## 运行方法

### 前提条件
- 后端服务已启动（http://localhost:8000）
- 数据库连接正常
- 测试用户存在：`jiangkuanli` / `123456`

### 运行命令

**1. 查看数据库表结构**
```bash
# 在 test_2.4-2.5 目录中运行
python show_table_structure.py
```

**2. 测试文档API接口**
```bash
# 在 test_2.4-2.5 目录中运行
python test_document_api.py
```



