"""
    @project: aihub
    @Author: jiangkuanli
    @file: documents
    @date: 2026/2/4
    @desc: Document management API routes
"""

import os
import uuid
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database.base import get_db
from app.schemas.document import (
    DocumentCreate, DocumentUpdate, DocumentResponse, DocumentListResponse,
    ParagraphResponse, DocumentDetailResponse, DocumentUploadResponse
)
from app.services.document_service import DocumentService
from app.services.auth_service import get_current_user
from app.services.minio_service import minio_service
from app.models.user import User

router = APIRouter()


@router.post("/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """上传文档并自动解析"""
    document_service = DocumentService(db)
    
    # 验证文件类型
    allowed_extensions = {'.pdf', '.doc', '.docx', '.txt', '.md', '.xls', '.xlsx'}
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的文件类型。支持的类型: {', '.join(allowed_extensions)}"
        )
    
    # 生成唯一文件名
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # 读取文件内容
    try:
        content = await file.read()
        file_size = len(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件读取失败: {str(e)}"
        )
    
    # 上传到MinIO
    try:
        minio_object_name = minio_service.upload_bytes(
            data=content,
            object_name=unique_filename,
            content_type=file.content_type,
            length=file_size
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件上传到MinIO失败: {str(e)}"
        )
    
    # 创建文档记录（存储MinIO对象名）
    document = document_service.create_document(
        user_id=current_user.id,
        filename=file.filename,
        file_path=minio_object_name,  # 存储MinIO对象名
        file_type=file_extension[1:],  # 去掉点号
        file_size=file_size,
        content_type=file.content_type
    )
    
    # 处理文档（解析、分段、存储）
    process_result = document_service.process_document(document.id, content)
    
    if not process_result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文档处理失败: {process_result.get('error')}"
        )
    
    return DocumentUploadResponse(
        document_id=document.id,
        message="文档上传成功",
        total_paragraphs=process_result["total_paragraphs"],
        total_characters=process_result["total_characters"]
    )


@router.get("", response_model=List[DocumentListResponse])
def list_documents(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=100, description="返回记录数"),
    status: str = Query(None, description="文档状态过滤"),
    file_type: str = Query(None, description="文件类型过滤"),
    search: str = Query(None, description="文件名搜索"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取文档列表（支持分页和筛选）"""
    document_service = DocumentService(db)
    documents = document_service.get_documents(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        status=status,
        file_type=file_type,
        search=search
    )
    return documents


@router.get("/{document_id}", response_model=DocumentDetailResponse)
def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取文档详情（包含段落）"""
    document_service = DocumentService(db)
    document = document_service.get_document(document_id, current_user.id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文档不存在"
        )
    
    paragraphs = document_service.get_paragraphs(document_id)
    
    return DocumentDetailResponse(
        id=document.id,
        user_id=document.user_id,
        filename=document.filename,
        file_path=document.file_path,
        file_type=document.file_type,
        file_size=document.file_size,
        content_type=document.content_type,
        chunk_size=document.chunk_size,
        chunk_overlap=document.chunk_overlap,
        splitter_type=document.splitter_type,
        total_paragraphs=document.total_paragraphs,
        status=document.status,
        error_message=document.error_message,
        is_active=document.is_active,
        created_at=document.created_at,
        updated_at=document.updated_at,
        paragraphs=paragraphs
    )


@router.get("/{document_id}/download")
def download_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """下载文档（从MinIO）"""
    document_service = DocumentService(db)
    document = document_service.get_document(document_id, current_user.id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文档不存在"
        )
    
    try:
        file_data = minio_service.download_file(document.file_path)
        
        return StreamingResponse(
            iter([file_data]),
            media_type=document.content_type,
            headers={
                "Content-Disposition": f"attachment; filename={document.filename}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件下载失败: {str(e)}"
        )


@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
    document_id: str,
    document_update: DocumentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新文档信息"""
    document_service = DocumentService(db)
    document = document_service.update_document(document_id, current_user.id, document_update)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文档不存在"
        )
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除文档"""
    document_service = DocumentService(db)
    success = document_service.delete_document(document_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文档不存在"
        )
    return None


@router.get("/{document_id}/paragraphs", response_model=List[ParagraphResponse])
def get_document_paragraphs(
    document_id: str,
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=100, description="返回记录数"),
    search: str = Query(None, description="段落内容搜索"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取文档的所有段落（支持分页和搜索）"""
    document_service = DocumentService(db)
    document = document_service.get_document(document_id, current_user.id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文档不存在"
        )
    
    paragraphs = document_service.get_paragraphs(
        document_id=document_id,
        skip=skip,
        limit=limit,
        search=search
    )
    return paragraphs


@router.get("/paragraphs/{paragraph_id}", response_model=ParagraphResponse)
def get_paragraph(
    paragraph_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取单个段落"""
    document_service = DocumentService(db)
    paragraph = document_service.get_paragraph(paragraph_id)
    if not paragraph:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="段落不存在"
        )
    
    # 验证段落所属文档是否属于当前用户
    document = document_service.get_document(paragraph.document_id, current_user.id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问该段落"
        )
    
    return paragraph
