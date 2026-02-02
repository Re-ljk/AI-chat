"""
    @project: aihub
    @Author: jiangkuanli
    @file: main
    @date: 2026/1/19 14:17
    @desc:
"""

import logging
import os
from pathlib import Path

import httpx
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import diskcache
from sqlalchemy.orm import Session

from app.common.core.result import AppApiException, Result
from app.database.base import get_db
from app.models import User
from app.services.auth_service import auth_token
from config import settings
from app.routers import api_v1


def api_exception_handler():
    """
    处理API异常
    :param request:
    :param exc:
    :return:
    """
    @app.exception_handler(AppApiException)
    async def app_api_exception_handler(request: Request, exc: AppApiException):
        # 转换为 Result 错误格式
        error_result = Result.error(
            message=exc.message,
            code=exc.code
        )
        return JSONResponse(
            status_code=exc.code,  # HTTP状态码
            content=error_result.to_dict()  # 统一响应格式
        )

    # 处理其他未捕获的异常（可选）
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        error_result = Result.error(
            message="服务器内部错误",
            code=500,
            data={"detail": str(exc)}  # 包含错误详情（生产环境可移除）
        )
        return JSONResponse(
            status_code=500,
            content=error_result.to_dict()
        )


def init_logger():
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)

# 配置日志
init_logger()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# 处理API异常
api_exception_handler()

# 设置CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# 包含路由
app.include_router(api_v1.router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PROJECT_PORT)
