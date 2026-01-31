"""
    @project: aihub
    @Author: dongrunhua
    @file: config
    @date: 2026/1/19 14:16
    @desc:
"""
from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import AnyUrl, Field


class Settings(BaseSettings):
    # 项目配置
    PROJECT_NAME: str = "baoxian"
    PROJECT_VERSION: str = "0.1.0"
    PROJECT_DESCRIPTION: str = "保险测试"  # 添加这行
    PROJECT_PORT: int = 8000

    # 数据库配置
    PG_HOST: str = "47.108.29.156"
    PG_PORT: int = 25432
    PG_USER: str = "baoxian_test"
    PG_PASSWORD: str = "baoxian@123"
    PG_DB: str = "baoxian_test01"

    # 日志配置
    LOG_LEVEL: str = "INFO"

    # API 配置
    API_V1_STR: str = "/api/v1"

    # PostgreSQL 配置
    ENV_DB_URL: AnyUrl = f"postgresql://{PG_USER}:{PG_PASSWORD.replace('@', '%%40')}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    DB_URL: AnyUrl = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    DB_POOL_SIZE: int = 200
    DB_MAX_OVERFLOW: int = 100

    # JWT 配置
    SECRET_KEY: str = "aw.1234567890"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 300  # 30分钟
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 7  # 7天

    # DeepSeek API 配置
    DEEPSEEK_API_KEY: str = "sk-34cb02de162f4804b08962a7cb58889e"
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL: str = "deepseek-chat"

    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]

    class Config:
        case_sensitive = True
        env_file = Path(__file__).resolve().parent / ".env"


settings = Settings()
