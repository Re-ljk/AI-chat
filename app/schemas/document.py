"""
    @project: aihub
    @Author: jiangkuanli
    @file: document
    @date: 2026/2/4
    @desc: Document and Paragraph schemas
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class DocumentBase(BaseModel):
    filename: str = Field(..., description="文件名")
    file_type: str = Field(..., description="文件类型")
    file_size: int = Field(..., description="文件大小（字节）")
    content_type: Optional[str] = Field(None, description="内容类型")
    chunk_size: Optional[int] = Field(None, description="分段大小")
    chunk_overlap: Optional[int] = Field(None, description="分段重叠")
    splitter_type: Optional[str] = Field(None, description="分段类型")


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None


class DocumentResponse(DocumentBase):
    id: str
    user_id: str
    file_path: str
    total_paragraphs: int
    status: str
    error_message: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    id: str
    user_id: str
    filename: str
    file_type: str
    file_size: int
    total_paragraphs: int
    status: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ParagraphBase(BaseModel):
    paragraph_index: int = Field(..., description="段落索引")
    content: str = Field(..., description="段落内容")
    character_count: int = Field(default=0, description="字符数")


class ParagraphCreate(ParagraphBase):
    document_id: str


class ParagraphUpdate(BaseModel):
    content: Optional[str] = None


class ParagraphResponse(ParagraphBase):
    id: str
    document_id: str
    para_metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentDetailResponse(DocumentResponse):
    paragraphs: List[ParagraphResponse] = Field(default_factory=list)


class DocumentUploadResponse(BaseModel):
    document_id: str
    message: str = "文档上传成功"
    total_paragraphs: int
    total_characters: int
