"""
    @project: aihub
    @Author: jiangkuanli
    @file: result
    @date: 2025/7/9 11:51
    @desc:
"""

import json


class Result:
    """统一API响应结果类"""

    def __init__(self, code: int, message: str, data=None):
        self.code = code
        self.message = message
        self.data = data

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "code": self.code,
            "message": self.message,
            "data": self.data
        }

    @staticmethod
    def success(data=None, message: str = "Success", code: int = 200) -> 'Result':
        """成功响应便捷方法"""
        return Result(code=code, message=message, data=data)

    @staticmethod
    def error(message: str = "Error", code: int = 500, data=None) -> 'Result':
        """错误响应便捷方法"""
        return Result(code=code, message=message, data=data)

    @staticmethod
    def validation_error(errors: list, message: str = "Validation Error", code: int = 422) -> 'Result':
        """验证错误便捷方法"""
        return Result(code=code, message=message, data={"errors": errors})

    @staticmethod
    def unauthorized(message: str = "Unauthorized", code: int = 401) -> 'Result':
        """未授权错误便捷方法"""
        return Result(code=code, message=message, data=None)

    @staticmethod
    def forbidden(message: str = "Forbidden", code: int = 403) -> 'Result':
        """禁止访问错误便捷方法"""
        return Result(code=code, message=message, data=None)

    @staticmethod
    def not_found(message: str = "Not Found", code: int = 404) -> 'Result':
        """未找到资源错误便捷方法"""
        return Result(code=code, message=message, data=None)

    @staticmethod
    def conflict(message: str = "Conflict", code: int = 409) -> 'Result':
        """资源冲突错误便捷方法"""
        return Result(code=code, message=message, data=None)


class AppApiException(Exception):
    """
    项目内异常
    """

    def __init__(self, code, message):
        self.code = code
        self.message = message


class StreamResult:

    @staticmethod
    def to_stream_chunk_response(code: int, content: str, is_end: bool=False, ensure_ascii=True):
        chunk = json.dumps({"code": code, "content": content, "operate": True, "is_end": is_end}, ensure_ascii=ensure_ascii)
        return 'data: ' + chunk + '\n\n'
