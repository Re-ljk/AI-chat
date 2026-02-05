"""
    @project: aihub
    @Author: jiangkuanli
    @file: test_minio_and_document_apis
    @date: 2026/2/5
    @desc: 测试MinIO集成和文档API接口
"""

import sys
import os
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import requests
import json
from typing import Dict, Any, Optional

# 配置日志
class Tee:
    """同时输出到控制台和文件"""
    def __init__(self, file_path):
        self.file = open(file_path, 'w', encoding='utf-8')
        self.stdout = sys.stdout
        sys.stdout = self
    
    def write(self, data):
        self.stdout.write(data)
        self.file.write(data)
    
    def flush(self):
        self.stdout.flush()
        self.file.flush()
    
    def close(self):
        sys.stdout = self.stdout
        self.file.close()

# 创建日志文件
log_file = Path(__file__).parent / "test_log.txt"
logger = Tee(log_file)


class APITester:
    """API测试器"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.user_id: Optional[str] = None
    
    def print_section(self, title: str):
        """打印测试区块"""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    
    def print_result(self, test_name: str, success: bool, message: str = ""):
        """打印测试结果"""
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{status} - {test_name}")
        if message:
            print(f"  {message}")
    
    def login(self, username: str = "jiangkuanli", password: str = "123456") -> bool:
        """登录获取token"""
        self.print_section("用户登录")
        
        try:
            # 使用form-encoded数据而不是JSON
            data = {
                "username": username,
                "password": password
            }
            
            response = requests.post(
                f"{self.base_url}/api/v1/auth/login",
                data=data
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                user_email = data.get("user_id") or data.get("sub")
                self.user_id = user_email
                self.print_result("用户登录", True, f"用户: {user_email}")
                return True
            else:
                self.print_result("用户登录", False, response.text)
                return False
        except Exception as e:
            self.print_result("用户登录", False, str(e))
            return False
    
    def get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def test_minio_service(self) -> bool:
        """测试MinIO服务"""
        self.print_section("测试MinIO服务")
        
        try:
            from app.services.minio_service import minio_service
            
            # 测试上传
            test_data = b"Hello MinIO! This is a test file."
            object_name = "test_file.txt"
            
            result = minio_service.upload_bytes(test_data, object_name, "text/plain", len(test_data))
            self.print_result("MinIO上传文件", True, f"对象名: {result}")
            
            # 测试下载
            downloaded_data = minio_service.download_file(object_name)
            download_success = downloaded_data == test_data
            self.print_result("MinIO下载文件", download_success, "数据匹配" if download_success else "数据不匹配")
            
            # 测试URL生成
            url = minio_service.get_presigned_url(object_name)
            self.print_result("MinIO生成URL", bool(url), f"URL: {url[:50]}..." if url else "URL为空")
            
            # 测试删除
            delete_success = minio_service.delete_file(object_name)
            self.print_result("MinIO删除文件", delete_success)
            
            return True
        except Exception as e:
            self.print_result("MinIO服务测试", False, str(e))
            return False
    
    def test_document_upload(self, file_path: str) -> Optional[str]:
        """测试文档上传"""
        self.print_section("测试文档上传")
        
        if not os.path.exists(file_path):
            self.print_result("文档上传", False, f"文件不存在: {file_path}")
            return None
        
        try:
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f, "application/octet-stream")}
                headers = {"Authorization": f"Bearer {self.token}"}
                
                response = requests.post(
                    f"{self.base_url}/api/v1/documents/upload",
                    files=files,
                    headers=headers
                )
                
                if response.status_code == 201:
                    data = response.json()
                    document_id = data.get("document_id")
                    self.print_result("文档上传", True, f"文档ID: {document_id}, 段落数: {data.get('total_paragraphs')}")
                    return document_id
                else:
                    self.print_result("文档上传", False, response.text)
                    return None
        except Exception as e:
            self.print_result("文档上传", False, str(e))
            return None
    
    def test_document_list(self, **filters) -> bool:
        """测试文档列表"""
        self.print_section("测试文档列表查询")
        
        try:
            params = {}
            if filters:
                params.update(filters)
            
            response = requests.get(
                f"{self.base_url}/api/v1/documents",
                headers=self.get_headers(),
                params=params
            )
            
            if response.status_code == 200:
                documents = response.json()
                self.print_result("文档列表查询", True, f"找到 {len(documents)} 个文档")
                for doc in documents[:3]:
                    print(f"  - {doc['filename']} ({doc['status']})")
                return True
            else:
                self.print_result("文档列表查询", False, response.text)
                return False
        except Exception as e:
            self.print_result("文档列表查询", False, str(e))
            return False
    
    def test_document_detail(self, document_id: str) -> bool:
        """测试文档详情"""
        self.print_section("测试文档详情查询")
        
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/documents/{document_id}",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_result("文档详情查询", True, f"文档: {data['filename']}, 段落数: {len(data.get('paragraphs', []))}")
                return True
            else:
                self.print_result("文档详情查询", False, response.text)
                return False
        except Exception as e:
            self.print_result("文档详情查询", False, str(e))
            return False
    
    def test_document_download(self, document_id: str) -> bool:
        """测试文档下载"""
        self.print_section("测试文档下载")
        
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/documents/{document_id}/download",
                headers=self.get_headers(),
                stream=True
            )
            
            if response.status_code == 200:
                file_size = len(response.content)
                self.print_result("文档下载", True, f"下载文件大小: {file_size} 字节")
                return True
            else:
                self.print_result("文档下载", False, response.text)
                return False
        except Exception as e:
            self.print_result("文档下载", False, str(e))
            return False
    
    def test_document_paragraphs(self, document_id: str, **filters) -> bool:
        """测试文档段落列表"""
        self.print_section("测试文档段落查询")
        
        try:
            params = {}
            if filters:
                params.update(filters)
            
            response = requests.get(
                f"{self.base_url}/api/v1/documents/{document_id}/paragraphs",
                headers=self.get_headers(),
                params=params
            )
            
            if response.status_code == 200:
                paragraphs = response.json()
                self.print_result("文档段落查询", True, f"找到 {len(paragraphs)} 个段落")
                for para in paragraphs[:3]:
                    content_preview = para['content'][:50] + "..." if len(para['content']) > 50 else para['content']
                    print(f"  - 段落 {para['paragraph_index']}: {content_preview}")
                return True
            else:
                self.print_result("文档段落查询", False, response.text)
                return False
        except Exception as e:
            self.print_result("文档段落查询", False, str(e))
            return False
    
    def test_document_delete(self, document_id: str) -> bool:
        """测试文档删除"""
        self.print_section("测试文档删除")
        
        try:
            response = requests.delete(
                f"{self.base_url}/api/v1/documents/{document_id}",
                headers=self.get_headers()
            )
            
            if response.status_code == 204:
                self.print_result("文档删除", True)
                return True
            else:
                self.print_result("文档删除", False, response.text)
                return False
        except Exception as e:
            self.print_result("文档删除", False, str(e))
            return False
    
    def run_all_tests(self, test_file: Optional[str] = None):
        """运行所有测试"""
        print("\n" + "="*60)
        print("  MinIO和文档API接口测试")
        print("="*60)
        
        # 登录
        if not self.login():
            print("\n登录失败，测试终止")
            return
        
        # 测试MinIO服务
        self.test_minio_service()
        
        # 测试文档上传
        document_id = None
        if test_file and os.path.exists(test_file):
            document_id = self.test_document_upload(test_file)
        else:
            print("\n跳过文档上传测试（未提供测试文件）")
        
        if document_id:
            # 测试文档列表
            self.test_document_list()
            
            # 测试带筛选的文档列表
            self.test_document_list(status="completed")
            self.test_document_list(file_type="txt")
            
            # 测试文档详情
            self.test_document_detail(document_id)
            
            # 测试文档下载
            self.test_document_download(document_id)
            
            # 测试文档段落
            self.test_document_paragraphs(document_id)
            
            # 测试带搜索的文档段落
            self.test_document_paragraphs(document_id, search="测试")
            
            # 测试文档删除
            self.test_document_delete(document_id)
        else:
            print("\n跳过文档相关测试（文档上传失败）")
        
        print("\n" + "="*60)
        print("  测试完成")
        print("="*60 + "\n")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="测试MinIO和文档API接口")
    parser.add_argument("--file", type=str, help="测试文件路径")
    parser.add_argument("--url", type=str, default="http://localhost:8000", help="API基础URL")
    
    args = parser.parse_args()
    
    tester = APITester(base_url=args.url)
    tester.run_all_tests(test_file=args.file)


if __name__ == "__main__":
    try:
        main()
    finally:
        # 关闭日志
        logger.close()
        print(f"\n日志已保存到: {log_file}")
