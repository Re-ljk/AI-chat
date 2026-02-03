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
- ✅ 图片提取（Word、Excel文档中的图片）

### 项目结构

```shell
├── alembic/                  # 数据库迁移
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── common/               # 公用模块
│   │   ├── code
│   │   └── utils
│   ├── database/
│   │   ├── __init__.py
│   │   └── base.py           # 数据库连接
│   ├── models/               # 数据库模型
│   │   ├── user.py
│   │   ├── session.py         # 会话模型
│   │   └── conversation.py   # AI对话模型
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── api_v1.py         # 接口路由配置
│   │   ├── users.py          # 用户路由接口
│   │   ├── auth.py           # 认证路由接口
│   │   ├── sessions.py        # 会话管理路由接口
│   │   └── conversations.py   # AI对话管理路由接口
│   ├── schemas/              # 接口数据模型定义
│   │   ├── __init__.py
│   │   ├── token.py
│   │   ├── user.py
│   │   ├── session.py         # 会话相关schemas
│   │   └── conversation.py   # AI对话相关schemas
│   ├── services/             # 业务逻辑实现层
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── auth_service.py   # 认证服务
│   │   ├── session_service.py  # 会话管理服务
│   │   ├── conversation_service.py  # AI对话管理服务
│   │   ├── langchain_service.py   # LangChain服务
│   │   ├── document_parsers/       # 文档解析器
│   │   │   ├── __init__.py
│   │   │   ├── base_parser.py      # 文档解析基类
│   │   │   ├── word_parser.py      # Word文档解析器
│   │   │   ├── excel_parser.py     # Excel文档解析器
│   │   │   ├── pdf_parser.py       # PDF文档解析器
│   │   │   ├── unstructured_parser.py  # Unstructured集成解析器
│   │   │   └── text_splitter.py    # 文本分段器
│   │   └── document_parser_service.py  # 文档解析服务
│   └── __init__.py
├── main.py                   # 主应用入口
├── config.py                 # 配置类
├── requirements.txt
├── .env                      # 配置项
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

### 后端功能

#### 1. 用户管理
- 用户注册
- 用户登录（JWT认证）
- 用户信息查询
- 用户信息更新

#### 2. 会话管理
- 创建新会话
- 删除会话
- 查询会话历史
- 会话状态管理

#### 3. AI对话管理
- 创建AI对话
- 删除AI对话
- 查询对话列表
- 查询对话详情
- 添加用户消息
- 添加AI助手回复
- 查询对话消息列表
- 流式问答接口（SSE）
- 保存流式消息
- 红对话列表（多轮会话）
- LangChain集成（对话历史学习）
- AI智能回复生成（DeepSeek API）
- 对话总结功能
- 对话上下文管理
- 对话更新（标题修改、置顶等）

#### 4. 文档解析
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

### 前端功能

#### 1. 用户认证
- 登录页面
- 注册页面
- JWT Token管理
- 自动登录

#### 2. 对话管理
- 对话列表展示
- 创建新对话
- 删除对话
- 对话搜索
- 对话重命名
- 对话置顶

#### 3. 消息功能
- 发送消息
- 流式响应展示
- 多轮对话界面
- 消息搜索（高亮显示）
- 消息导出
- 消息复制
- 重新生成回复
- 停止生成

#### 4. UI/UX功能
- Markdown渲染（代码高亮）
- 表情选择器
- 设置面板（主题切换、字体大小调整）
- 文件上传
- 键盘快捷键
- 消息通知
- 响应式布局
- 仿照kimiUI设计风格

## 环境要求

### 后端
- Python 3.8+
- PostgreSQL 12+
- pip

### 前端
- Node.js 16+
- npm 或 yarn

## 安装步骤

### 1. 克隆项目

```bash
git clone -b ai_chat_g2_jiangkuanli http://47.108.29.156/baoxian_backend/backendLearning.git
cd backendLearning
```

### 2. 后端安装

#### 2.1 创建虚拟环境

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 2.2 安装依赖

```bash
pip install -r requirements.txt
```

#### 2.3 配置环境变量

创建 `.env` 文件，配置以下内容：

```env
# 数据库配置
PG_HOST=47.108.29.156
PG_PORT=25432
PG_USER=baoxian_test
PG_PASSWORD=baoxian@123
PG_DB=baoxian_test01

# JWT配置
SECRET_KEY=change_me_to_a_long_random_string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=300

# DeepSeek API配置
DEEPSEEK_API_KEY=your-deepseek-api-key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
```

#### 2.4 创建数据库

```sql
create database baoxian_test01;
```

#### 2.5 数据库迁移

```bash
# 初始化Alembic（如果还没有初始化）
alembic init alembic

# 创建迁移文件
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head
```

### 3. 前端安装

#### 3.1 进入前端目录

```bash
cd frontend
```

#### 3.2 安装依赖

```bash
npm install
```

#### 3.3 配置API地址

编辑 `frontend/src/services/api.ts`，确保API地址正确：

```typescript
const API_BASE_URL = 'http://localhost:8000/api/v1'
```

## 运行步骤

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

## 使用说明

### 1. 注册账号

- 访问 `http://localhost:3000/register`
- 填写用户名、邮箱、密码等信息
- 点击注册按钮

### 2. 登录系统

- 访问 `http://localhost:3000/login`
- 输入用户名和密码
- 点击登录按钮

### 3. 创建对话

- 登录后，点击左侧的"新建对话"按钮
- 或使用快捷键 `Ctrl + N`

### 4. 发送消息

- 在输入框中输入消息
- 按 `Enter` 键发送
- 或点击发送按钮

### 5. 使用快捷键

- `Ctrl + K`: 搜索对话
- `Ctrl + N`: 新建对话
- `Ctrl + E`: 导出对话
- `Enter`: 发送消息
- `Shift + Enter`: 换行

### 6. 其他功能

- 点击设置图标可以切换主题和调整字体大小
- 点击表情图标可以选择表情
- 点击附件图标可以上传文件
- 点击对话的编辑图标可以重命名对话
- 点击对话的图钉图标可以置顶对话
- 点击消息的复制图标可以复制消息内容
- 点击重新生成按钮可以重新生成AI回复
- 点击停止按钮可以停止正在生成的回复

### 7. 文档解析

#### 7.1 解析Word文档

```python
from app.services.document_parser_service import document_parser_service

result = document_parser_service.parse_document('test.docx')
print(result['content'])
print(result['metadata'])
```

#### 7.2 解析Excel文档

```python
result = document_parser_service.parse_document('test.xlsx')
print(result['content'])
print(result['metadata'])
```

#### 7.3 解析PDF文档

```python
result = document_parser_service.parse_document('test.pdf')
print(result['content'])
print(result['metadata'])
```

#### 7.4 使用Unstructured解析

```python
result = document_parser_service.parse_document('test.docx')
print(result['content'])
print(result['metadata'])
```

#### 7.5 文本分段

```python
chunks = document_parser_service.split_document(
    text,
    metadata={'source': 'test.txt'},
    split_method='recursive_char',
    chunk_size=1000,
    chunk_overlap=200
)
```

#### 7.6 解析并分段

```python
result = document_parser_service.parse_and_split(
    'test.docx',
    split_method='recursive_char',
    chunk_size=1000,
    chunk_overlap=200
)
```

#### 7.7 提取文档中的图片

```python
from app.services.document_parser_service import document_parser_service
import base64

result = document_parser_service.parse_document('test.docx')

if result['success']:
    # 检查是否包含图片
    if result['metadata'].get('has_images', False):
        print(f"文档包含 {result['metadata'].get('image_count', 0)} 张图片")
        
        # 遍历所有图片
        for img in result['images']:
            print(f"图片 {img['index']}:")
            print(f"  - 扩展名: {img['extension']}")
            print(f"  - 大小: {img['size']} bytes")
            
            # 保存图片到文件
            image_data = base64.b64decode(img['data'])
            with open(f"image_{img['index']}.{img['extension']}", 'wb') as f:
                f.write(image_data)
```

## API文档

启动后端服务后，访问以下地址查看API文档：

- Swagger UI: `http://0.0.0.0:8000/api/v1/docs`
- ReDoc: `http://0.0.0.0:8000/api/v1/redoc`

## 技术栈

### 后端
- FastAPI - Web框架
- SQLAlchemy - ORM
- PostgreSQL - 数据库
- Alembic - 数据库迁移
- Pydantic - 数据验证
- LangChain - AI对话管理
- DeepSeek API - AI模型
- Unstructured - 文档解析

### 前端
- React - UI框架
- TypeScript - 类型系统
- Vite - 构建工具
- Ant Design - UI组件库
- React Router - 路由管理
- Axios - HTTP客户端
- React Markdown - Markdown渲染
- React Syntax Highlighter - 代码高亮
- Emoji Picker React - 表情选择器
