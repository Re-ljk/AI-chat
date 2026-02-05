"""
    @project: aihub
    @Author: jiangkuanli
    @file: minio_service
    @date: 2026/2/6
    @desc: MinIO对象存储服务
"""

from minio import Minio
from minio.error import S3Error
from io import BytesIO
from pathlib import Path
from typing import Optional
from datetime import timedelta
import logging

from config import settings

logger = logging.getLogger(__name__)


class MinIOService:
    def __init__(self):
        self.client = Minio(
            endpoint=settings.MINIO_ENDPOINT_URL,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """确保存储桶存在"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"创建存储桶: {self.bucket_name}")
            else:
                logger.info(f"存储桶已存在: {self.bucket_name}")
        except S3Error as e:
            logger.error(f"检查/创建存储桶失败: {e}")
            raise

    def upload_file(
        self,
        file_path: str,
        object_name: Optional[str] = None,
        content_type: Optional[str] = "application/octet-stream"
    ) -> str:
        """
        上传文件到MinIO

        Args:
            file_path: 本地文件路径
            object_name: MinIO中的对象名（可选，默认使用文件名）
            content_type: 内容类型

        Returns:
            MinIO中的对象名
        """
        try:
            if object_name is None:
                object_name = Path(file_path).name

            self.client.fput_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                file_path=file_path,
                content_type=content_type
            )

            logger.info(f"文件上传成功: {object_name}")
            return object_name

        except S3Error as e:
            logger.error(f"文件上传失败: {e}")
            raise

    def upload_bytes(
        self,
        data: bytes,
        object_name: str,
        content_type: Optional[str] = "application/octet-stream",
        length: Optional[int] = None
    ) -> str:
        """
        上传字节数据到MinIO

        Args:
            data: 字节数据
            object_name: MinIO中的对象名
            content_type: 内容类型
            length: 数据长度

        Returns:
            MinIO中的对象名
        """
        try:
            data_stream = BytesIO(data)
            if length is None:
                length = len(data)

            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=data_stream,
                length=length,
                content_type=content_type
            )

            logger.info(f"字节数据上传成功: {object_name}")
            return object_name

        except S3Error as e:
            logger.error(f"字节数据上传失败: {e}")
            raise

    def download_file(
        self,
        object_name: str,
        file_path: Optional[str] = None
    ) -> bytes:
        """
        从MinIO下载文件

        Args:
            object_name: MinIO中的对象名
            file_path: 本地保存路径（可选）

        Returns:
            文件字节数据
        """
        try:
            response = self.client.get_object(
                bucket_name=self.bucket_name,
                object_name=object_name
            )

            data = response.read()

            if file_path:
                Path(file_path).parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, "wb") as f:
                    f.write(data)
                logger.info(f"文件下载成功: {object_name} -> {file_path}")
            else:
                logger.info(f"文件下载成功: {object_name}")

            return data

        except S3Error as e:
            logger.error(f"文件下载失败: {e}")
            raise

    def delete_file(self, object_name: str) -> bool:
        """
        从MinIO删除文件

        Args:
            object_name: MinIO中的对象名

        Returns:
            是否删除成功
        """
        try:
            self.client.remove_object(
                bucket_name=self.bucket_name,
                object_name=object_name
            )
            logger.info(f"文件删除成功: {object_name}")
            return True

        except S3Error as e:
            logger.error(f"文件删除失败: {e}")
            return False

    def file_exists(self, object_name: str) -> bool:
        """
        检查文件是否存在

        Args:
            object_name: MinIO中的对象名

        Returns:
            文件是否存在
        """
        try:
            self.client.stat_object(
                bucket_name=self.bucket_name,
                object_name=object_name
            )
            return True

        except S3Error as e:
            if e.code == "NoSuchKey":
                return False
            logger.error(f"检查文件存在性失败: {e}")
            raise

    def get_file_url(self, object_name: str, expires: int = 3600) -> str:
        """
        获取文件的预签名URL

        Args:
            object_name: MinIO中的对象名
            expires: URL过期时间（秒），默认1小时

        Returns:
            预签名的文件URL
        """
        try:
            url = self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                expires=timedelta(seconds=expires)
            )
            logger.info(f"生成文件URL: {url}")
            return url
        except S3Error as e:
            logger.error(f"生成文件URL失败: {e}")
            raise
    
    def get_presigned_url(self, object_name: str, expires: int = 3600) -> str:
        """
        获取文件的预签名URL（别名方法）

        Args:
            object_name: MinIO中的对象名
            expires: URL过期时间（秒），默认1小时

        Returns:
            预签名的文件URL
        """
        return self.get_file_url(object_name, expires)

    def list_files(self, prefix: Optional[str] = None, recursive: bool = False) -> list:
        """
        列出存储桶中的文件

        Args:
            prefix: 对象名前缀
            recursive: 是否递归列出

        Returns:
            文件列表
        """
        try:
            objects = self.client.list_objects(
                bucket_name=self.bucket_name,
                prefix=prefix,
                recursive=recursive
            )
            return [obj.object_name for obj in objects]

        except S3Error as e:
            logger.error(f"列出文件失败: {e}")
            raise


minio_service = MinIOService()