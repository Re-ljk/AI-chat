# 项目结构
```shell
├── alembic/                  # 数据库迁移
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── common/               # 公用模块
│   │   ├── code
│   │   ├── utils
│   ├── database/
│   │   ├── __init__.py
│   │   ├── base.py           # 数据库连接
│   ├── models/               # 数据库实例
│   │   └── user.py  
│   │   └── ... 
│   ├── routers/
│   │   ├── __init__.py       
│   │   ├── api_v1.py         # 接口路由配置
│   │   ├── users.py          # user路由接口 view层
│   │   └── auth.py           # auth路由接口 view层
│   ├── schemas/              # 接口路由层，request、response 元数据定义
│   │   ├── __init__.py
│   │   ├── token.py          
│   │   ├── user.py
│   ├── services/             # 业务具体实现层
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── auth_service.py   # 认证服务
│   ├── __init__.py
├── main.py                   # 主类，启动类
├── config.py                 # 配置类
├── requirements.txt
├── .env                      # 配置项
├── alembic.ini
└── README.md
```

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




