"""
    @project: aihub
    @Author: jiangkuanli
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
    PROJECT_DESCRIPTION: str = "保险测试"
    PROJECT_PORT: int = 8000

    # 数据库配置（从环境变量读取）
    PG_HOST: str = Field(..., env="PG_HOST")
    PG_PORT: int = Field(5432, env="PG_PORT")
    PG_USER: str = Field(..., env="PG_USER")
    PG_PASSWORD: str = Field(..., env="PG_PASSWORD")
    PG_DB: str = Field(..., env="PG_DB")

    # 日志配置
    LOG_LEVEL: str = "INFO"

    # API 配置
    API_V1_STR: str = "/api/v1"

    # PostgreSQL URL
    DB_URL: AnyUrl = Field(..., env="DB_URL")
    DB_POOL_SIZE: int = 200
    DB_MAX_OVERFLOW: int = 100

    # JWT 配置
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 300
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 7

    # DeepSeek API 配置
    DEEPSEEK_API_KEY: str = Field(..., env="DEEPSEEK_API_KEY")
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL: str = "deepseek-chat"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    class Config:
        case_sensitive = True
        env_file = Path(__file__).resolve().parent / ".env"


settings = Settings()
