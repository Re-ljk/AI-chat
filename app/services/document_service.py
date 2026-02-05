"""
    @project: aihub
    @Author: jiangkuanli
    @file: document_service
    @date: 2026/2/4
    @desc: Document and Paragraph CRUD operations
"""

import os
import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from app.models.document import Document, Paragraph
from app.schemas.document import (
    DocumentCreate, DocumentUpdate, ParagraphCreate, ParagraphUpdate,
    DocumentResponse, DocumentListResponse, ParagraphResponse, DocumentDetailResponse
)
from app.services.document_parser_service import document_parser_service


class DocumentService:
    """文档服务类"""

    def __init__(self, db: Session):
        self.db = db

    def create_document(
        self,
        user_id: str,
        filename: str,
        file_path: str,
        file_type: str,
        file_size: int,
        content_type: Optional[str] = None,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        splitter_type: Optional[str] = None
    ) -> Document:
        """创建文档记录"""
        document = Document(
            id=str(uuid.uuid4()),
            user_id=user_id,
            filename=filename,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
            content_type=content_type,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            splitter_type=splitter_type,
            status="processing"
        )
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def get_document(self, document_id: str, user_id: str) -> Optional[Document]:
        """获取单个文档"""
        return self.db.query(Document).filter(
            and_(Document.id == document_id, Document.user_id == user_id)
        ).first()

    def get_documents(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        file_type: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Document]:
        """获取文档列表（支持多种筛选）"""
        query = self.db.query(Document).filter(Document.user_id == user_id)
        
        if status:
            query = query.filter(Document.status == status)
        
        if file_type:
            query = query.filter(Document.file_type == file_type)
        
        if search:
            query = query.filter(Document.filename.contains(search))
        
        return query.order_by(desc(Document.created_at)).offset(skip).limit(limit).all()

    def update_document(
        self,
        document_id: str,
        user_id: str,
        document_update: DocumentUpdate
    ) -> Optional[Document]:
        """更新文档"""
        document = self.get_document(document_id, user_id)
        if not document:
            return None

        update_data = document_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(document, field, value)

        self.db.commit()
        self.db.refresh(document)
        return document

    def delete_document(self, document_id: str, user_id: str) -> bool:
        """删除文档"""
        document = self.get_document(document_id, user_id)
        if not document:
            return False

        self.db.delete(document)
        self.db.commit()
        return True

    def update_document_status(
        self,
        document_id: str,
        status: str,
        total_paragraphs: Optional[int] = None,
        error_message: Optional[str] = None
    ) -> Optional[Document]:
        """更新文档状态"""
        document = self.db.query(Document).filter(Document.id == document_id).first()
        if not document:
            return None

        document.status = status
        if total_paragraphs is not None:
            document.total_paragraphs = total_paragraphs
        if error_message is not None:
            document.error_message = error_message

        self.db.commit()
        self.db.refresh(document)
        return document

    def create_paragraph(
        self,
        document_id: str,
        paragraph_index: int,
        content: str,
        para_metadata: Optional[Dict[str, Any]] = None
    ) -> Paragraph:
        """创建段落"""
        paragraph = Paragraph(
            id=str(uuid.uuid4()),
            document_id=document_id,
            paragraph_index=paragraph_index,
            content=content,
            character_count=len(content),
            para_metadata=para_metadata or {}
        )
        self.db.add(paragraph)
        self.db.commit()
        self.db.refresh(paragraph)
        return paragraph

    def get_paragraphs(
        self,
        document_id: str,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> List[Paragraph]:
        """获取文档的所有段落（支持分页和搜索）"""
        query = self.db.query(Paragraph).filter(Paragraph.document_id == document_id)
        
        if search:
            query = query.filter(Paragraph.content.contains(search))
        
        return query.order_by(Paragraph.paragraph_index).offset(skip).limit(limit).all()

    def get_paragraph(self, paragraph_id: str) -> Optional[Paragraph]:
        """获取单个段落"""
        return self.db.query(Paragraph).filter(Paragraph.id == paragraph_id).first()

    def update_paragraph(
        self,
        paragraph_id: str,
        paragraph_update: ParagraphUpdate
    ) -> Optional[Paragraph]:
        """更新段落"""
        paragraph = self.get_paragraph(paragraph_id)
        if not paragraph:
            return None

        update_data = paragraph_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(paragraph, field, value)

        if paragraph_update.content:
            paragraph.character_count = len(paragraph_update.content)

        self.db.commit()
        self.db.refresh(paragraph)
        return paragraph

    def delete_paragraph(self, paragraph_id: str) -> bool:
        """删除段落"""
        paragraph = self.get_paragraph(paragraph_id)
        if not paragraph:
            return False

        self.db.delete(paragraph)
        self.db.commit()
        return True

    def process_document(
        self,
        document_id: str,
        file_content: bytes
    ) -> Dict[str, Any]:
        """处理文档：解析、分段、存储"""
        try:
            document = self.db.query(Document).filter(Document.id == document_id).first()
            if not document:
                return {"success": False, "error": "文档不存在"}

            # 解析文档（从字节数据）
            parse_result = document_parser_service.parse_document_from_bytes(file_content, document.file_type)
            
            if not parse_result.get("success"):
                self.update_document_status(document_id, "failed", error_message=parse_result.get("error", "解析失败"))
                return {"success": False, "error": parse_result.get("error", "解析失败")}

            # 分段
            paragraphs = document_parser_service.split_document(
                parse_result["content"],
                parse_result.get("metadata", {})
            )
            
            if not paragraphs:
                self.update_document_status(document_id, "failed", error_message="分段失败")
                return {"success": False, "error": "分段失败"}

            # 存储段落
            for idx, para in enumerate(paragraphs):
                self.create_paragraph(
                    document_id=document_id,
                    paragraph_index=idx,
                    content=para.get("content", ""),
                    para_metadata=para.get("metadata", {})
                )

            # 更新文档状态
            self.update_document_status(
                document_id,
                "completed",
                total_paragraphs=len(paragraphs)
            )

            return {
                "success": True,
                "total_paragraphs": len(paragraphs),
                "total_characters": len(parse_result.get("content", ""))
            }

        except Exception as e:
            self.update_document_status(document_id, "failed", error_message=str(e))
            return {"success": False, "error": str(e)}
