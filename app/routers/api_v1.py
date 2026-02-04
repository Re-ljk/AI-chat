"""
    @project: aihub
    @Author: dongrunhua
    @file: api_v1
    @date: 2025/7/8 17:56
    @desc:
"""
from fastapi import APIRouter
from app.routers import users, auth, sessions, conversations, documents

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
router.include_router(documents.router, prefix="/documents", tags=["documents"])

