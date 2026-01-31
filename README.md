# 项目结构
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
│   │   └── conversation_service.py  # AI对话管理服务
│   └── __init__.py
├── main.py                   # 主应用入口
├── config.py                 # 配置类
├── requirements.txt
├── .env                      # 配置项
├── alembic.ini
└── README.md
```

# 功能特性

## 1. 用户管理
- 用户注册
- 用户登录（JWT认证）
- 用户信息查询
- 用户信息更新

## 2. 会话管理
- 创建新会话
- 删除会话
- 查询会话历史
- 会话状态管理

## 3. AI对话管理
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
- AI智能回复生成
- 对话总结功能
- 对话上下文管理

# 创建数据库
```sql
create database baoxian_test01;
```

# 数据库迁移设置
初始化 Alembic & 创建迁移文件：
```shell
alembic init alembic

alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```




