"""
    @project: aihub
    @Author: jiangkuanli
    @file: test_document_api
    @date: 2026/2/4
    @desc: Document API test script
"""

import os
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"


def test_document_api():
    """测试文档管理API"""
    
    print("=" * 60)
    print("文档管理API测试")
    print("=" * 60)
    
    # 1. 登录获取token
    print("\n1. 登录获取token...")
    login_data = {
        "username": "jiangkuanli",
        "password": "123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}
            print("✓ 登录成功")
        else:
            print(f"✗ 登录失败: {response.status_code}")
            print(response.text)
            return
    except Exception as e:
        print(f"✗ 登录请求失败: {str(e)}")
        return
    
    # 2. 上传文档
    print("\n2. 上传文档...")
    
    # 创建测试文档
    test_file_path = "test_document.txt"
    test_content = """这是一个测试文档。

第一段：人工智能（Artificial Intelligence，简称AI）是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。

第二段：机器学习是人工智能的核心，是使计算机具有智能的根本途径。机器学习的基本思想是通过数据训练模型，使模型能够对新的数据进行预测或决策。

第三段：深度学习是机器学习的一个子集，它基于人工神经网络，尤其是多层神经网络。深度学习在图像识别、自然语言处理等领域取得了重大突破。

第四段：自然语言处理（NLP）是人工智能的重要应用领域，它研究如何让计算机理解和生成人类语言。

第五段：计算机视觉是另一个重要的AI应用领域，它致力于让计算机能够"看懂"图像和视频。
"""
    
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(test_content)
    
    try:
        with open(test_file_path, "rb") as f:
            files = {"file": ("test_document.txt", f, "text/plain")}
            response = requests.post(
                f"{BASE_URL}/documents/upload",
                files=files,
                headers=headers
            )
        
        if response.status_code == 201:
            upload_result = response.json()
            document_id = upload_result["document_id"]
            print(f"✓ 文档上传成功")
            print(f"  - 文档ID: {document_id}")
            print(f"  - 段落数: {upload_result['total_paragraphs']}")
            print(f"  - 字符数: {upload_result['total_characters']}")
        else:
            print(f"✗ 文档上传失败: {response.status_code}")
            print(response.text)
            return
    except Exception as e:
        print(f"✗ 文档上传请求失败: {str(e)}")
        return
    finally:
        if os.path.exists(test_file_path):
            try:
                os.remove(test_file_path)
            except PermissionError:
                print(f"⚠ 警告：无法删除测试文件 {test_file_path}，请手动删除")
    
    # 3. 获取文档列表
    print("\n3. 获取文档列表...")
    try:
        response = requests.get(f"{BASE_URL}/documents", headers=headers)
        if response.status_code == 200:
            documents = response.json()
            print(f"✓ 获取文档列表成功")
            print(f"  - 文档总数: {len(documents)}")
            for doc in documents:
                print(f"    - {doc['filename']} ({doc['file_type']}) - {doc['status']}")
        else:
            print(f"✗ 获取文档列表失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ 获取文档列表请求失败: {str(e)}")
    
    # 4. 获取文档详情
    print("\n4. 获取文档详情...")
    try:
        response = requests.get(f"{BASE_URL}/documents/{document_id}", headers=headers)
        if response.status_code == 200:
            document_detail = response.json()
            print(f"✓ 获取文档详情成功")
            print(f"  - 文件名: {document_detail['filename']}")
            print(f"  - 文件类型: {document_detail['file_type']}")
            print(f"  - 文件大小: {document_detail['file_size']} 字节")
            print(f"  - 段落数: {document_detail['total_paragraphs']}")
            print(f"  - 状态: {document_detail['status']}")
            print(f"  - 创建时间: {document_detail['created_at']}")
        else:
            print(f"✗ 获取文档详情失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ 获取文档详情请求失败: {str(e)}")
    
    # 5. 获取文档段落
    print("\n5. 获取文档段落...")
    try:
        response = requests.get(
            f"{BASE_URL}/documents/{document_id}/paragraphs",
            headers=headers
        )
        if response.status_code == 200:
            paragraphs = response.json()
            print(f"✓ 获取文档段落成功")
            print(f"  - 段落总数: {len(paragraphs)}")
            for idx, para in enumerate(paragraphs[:3], 1):  # 只显示前3个段落
                print(f"    - 段落{idx}: {para['content'][:50]}...")
                print(f"      字符数: {para['character_count']}")
            if len(paragraphs) > 3:
                print(f"    ... 还有 {len(paragraphs) - 3} 个段落")
        else:
            print(f"✗ 获取文档段落失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ 获取文档段落请求失败: {str(e)}")
    
    # 6. 更新文档
    print("\n6. 更新文档...")
    try:
        update_data = {
            "status": "archived"
        }
        response = requests.put(
            f"{BASE_URL}/documents/{document_id}",
            json=update_data,
            headers=headers
        )
        if response.status_code == 200:
            updated_doc = response.json()
            print(f"✓ 文档更新成功")
            print(f"  - 文档ID: {updated_doc['id']}")
            print(f"  - 文件名: {updated_doc['filename']}")
            print(f"  - 新状态: {updated_doc['status']}")
        else:
            print(f"✗ 文档更新失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ 文档更新请求失败: {str(e)}")
    
    # 7. 删除文档
    print("\n7. 删除文档...")
    try:
        response = requests.delete(
            f"{BASE_URL}/documents/{document_id}",
            headers=headers
        )
        if response.status_code == 204:
            print("✓ 删除文档成功")
        else:
            print(f"✗ 删除文档失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ 删除文档请求失败: {str(e)}")
    
    # 8. 验证删除
    print("\n8. 验证文档已删除...")
    try:
        response = requests.get(f"{BASE_URL}/documents/{document_id}", headers=headers)
        if response.status_code == 404:
            print("✓ 文档已成功删除")
        else:
            print(f"✗ 文档删除验证失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 验证删除请求失败: {str(e)}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_document_api()
