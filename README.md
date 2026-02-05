
## 项目展示

### 登录页面

![image-20260131164710796](./assets/image-20260131164710796.png)

简洁现代的登录界面，支持用户名和密码登录，集成 JWT 认证机制，保障用户身份安全。

### 注册页面

![image-20260131164736185](./assets/image-20260131164736185.png)

用户注册页面，包含用户名、邮箱、密码等信息校验，支持基础表单验证与错误提示。

### 对话管理页面

![image-20260131164828767](./assets/image-20260131164828767.png)

包含：
- 左侧对话列表（支持搜索、置顶、重命名、删除）
- 右侧消息展示区域（支持Markdown渲染、代码高亮）
- 底部输入框（支持表情选择、文件上传、快捷键）
- 设置面板（主题切换、字体大小调整）

### 核心功能

- ✅ 多轮对话支持
- ✅ 流式AI回复
- ✅ LangChain集成（对话历史学习）
- ✅ DeepSeek API集成
- ✅ 对话总结和上下文管理
- ✅ 消息搜索和高亮
- ✅ 对话导出
- ✅ 键盘快捷键
- ✅ 响应式设计
- ✅ 文档解析（Word、Excel、PDF）
- ✅ 文档分段（递归字符、Markdown标题、代码语法）
- ✅ 图片提取（Word、Excel、PDF文档中的图片）
- ✅ 文档上传和管理
- ✅ 文档自动分段和存储
- ✅ 段落查询和管理
- ✅ 文档状态跟踪
- ✅ MinIO对象存储集成
- ✅ 文档存储到MinIO
- ✅ 从MinIO下载原文
- ✅ MinIO预签名URL生成
- ✅ 完整的MinIO客户端操作

## 项目结构

```shell
├── alembic/                  # 数据库迁移
│   ├── versions/
│   │   └── add_document_tables.py  # 文档表迁移脚本
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── common/               # 公用模块
│   ├── database/              # 数据库连接
│   ├── models/                # 数据库模型
│   │   ├── user.py
│   │   ├── session.py
│   │   ├── conversation.py
│   │   └── document.py       # 文档和段落模型
│   ├── routers/               # API路由
│   │   ├── api_v1.py
│   │   ├── users.py
│   │   ├── auth.py
│   │   ├── sessions.py
│   │   ├── conversations.py
│   │   └── documents.py      # 文档管理API
│   ├── schemas/              # 数据模型定义
│   │   ├── token.py
│   │   ├── user.py
│   │   ├── session.py
│   │   ├── conversation.py
│   │   └── document.py       # 文档相关Schema
│   ├── services/             # 业务逻辑实现
│   │   ├── user_service.py
│   │   ├── auth_service.py
│   │   ├── session_service.py
│   │   ├── conversation_service.py
│   │   ├── langchain_service.py
│   │   ├── document_service.py      # 文档服务
│   │   ├── minio_service.py         # MinIO对象存储服务
│   │   ├── document_parsers/         # 文档解析器
│   │   │   ├── base_parser.py
│   │   │   ├── pdf_parser.py
│   │   │   ├── word_parser.py
│   │   │   ├── excel_parser.py
│   │   │   ├── text_splitter.py
│   │   │   └── unstructured_parser.py
│   │   └── document_parser_service.py
│   └── __init__.py
├── uploads/                  # 上传文件存储目录
├── nltk_data/               # NLTK数据目录
├── main.py                   # 主应用入口
├── config.py                 # 配置类
├── requirements.txt
├── .env
├── .gitignore
├── alembic.ini
├── frontend/                 # 前端项目（React + TypeScript + Vite）
│   ├── src/
│   │   ├── pages/          # 页面组件
│   │   │   ├── Login.tsx
│   │   │   ├── Register.tsx
│   │   │   └── Chat.tsx
│   │   ├── services/        # API服务
│   │   │   └── api.ts
│   │   ├── hooks/          # 自定义Hooks
│   │   │   └── useAuth.ts
│   │   ├── types/          # TypeScript类型定义
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── index.html
└── README.md
```

## 后端功能

### 1. 用户管理
- 用户注册
- 用户登录（JWT认证）
- 用户信息查询
- 用户信息更新

### 2. 会话管理
- 创建新会话
- 删除会话
- 查询会话历史
- 会话状态管理

### 3. AI对话管理
- 创建AI对话
- 删除AI对话
- 查询对话列表
- 查询对话详情
- 添加用户消息
- 添加AI助手回复
- 查询对话消息列表
- 流式问答接口（SSE）
- 保存流式消息
- LangChain集成（对话历史学习）
- AI智能回复生成（DeepSeek API）
- 对话总结功能
- 对话上下文管理
- 对话更新（标题修改、置顶等）

### 4. 文档解析
- Word文档解析（.docx, .doc）
- Excel文档解析（.xlsx, .xls, .csv）
- PDF文档解析（.pdf）
- Unstructured集成解析
- 文档元数据提取
- 递归字符分段
- Markdown标题分段
- 代码语法分段（Python/JS）
- 文档解析和分段一体化接口
- 图片提取（Word、Excel、PDF文档中的图片，Base64编码）

### 5. 文档管理
- 文档上传（支持多种格式：.txt, .docx, .doc, .xlsx, .xls, .csv, .pdf）
- 文档列表查询（分页、筛选）
- 文档详情查询
- 文档更新（状态、标题等）
- 文档删除
- 段落管理（查询、统计、搜索）
- 文档状态跟踪（processing/completed/failed/archived）
- 自动文档解析和分段
- 错误处理和日志记录
- **MinIO对象存储集成**
  - 文档自动上传到MinIO
  - 从MinIO下载原文
  - MinIO预签名URL生成
  - 完整的MinIO客户端操作
- 文件存储管理

## 前端功能

### 1. 用户认证
- 登录页面
- 注册页面
- JWT Token管理
- 自动登录

### 2. 对话管理
- 对话列表展示
- 创建新对话
- 删除对话
- 对话搜索
- 对话重命名
- 对话置顶

### 3. 消息功能
- 发送消息
- 流式响应展示
- 多轮对话界面
- 消息搜索（高亮显示）
- 消息导出
- 消息复制
- 重新生成回复
- 停止生成

### 4. UI/UX功能
- Markdown渲染（代码高亮）
- 表情选择器
- 设置面板（主题切换、字体大小调整）
- 文件上传
- 键盘快捷键
- 消息通知
- 响应式布局
- 仿照kimiUI设计风格

### 5. 文档功能
- 文档上传界面
- 文档列表展示
- 文档详情查看
- 段落管理
- 文档状态显示
- 文档搜索和筛选
- 文档删除和归档

## 启动步骤

### 1. 启动后端服务

在项目根目录下：

```bash
# 激活虚拟环境
venv\Scripts\activate  # Windows
# 或
source venv/bin/activate  # Linux/Mac

# 启动FastAPI服务器
python main.py
```

后端服务将在 `http://0.0.0.0:8000` 启动

### 2. 启动前端服务

在 `frontend` 目录下：

```bash
cd frontend
npm run dev
```

前端服务将在 `http://localhost:3000` 启动

### 3. 访问应用

打开浏览器，访问 `http://localhost:3000`
