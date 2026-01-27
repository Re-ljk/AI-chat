"""
    @project: aihub
    @Author: dongrunhua
    @file: api_v1
    @date: 2025/7/8 17:56
    @desc:
"""
from fastapi import APIRouter
from app.routers import users, auth, sessions

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])

