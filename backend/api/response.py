from typing import Any, Dict, Optional
from flask import jsonify


class APIResponse:
    """统一的API响应类，用于标准化所有API端点的返回格式"""
    
    @staticmethod
    def success(data: Any = None, message: str = None) -> tuple:
        """成功响应
        
        Args:
            data: 响应数据
            message: 成功消息
            
        Returns:
            tuple: (响应体, 状态码)
        """
        response = {
            'success': True
        }
        
        if data is not None:
            response['data'] = data
            
        if message:
            response['message'] = message
            
        return jsonify(response), 200
    
    @staticmethod
    def error(error: str, details: str = None, status_code: int = 500) -> tuple:
        """错误响应
        
        Args:
            error: 错误消息
            details: 错误详情
            status_code: HTTP状态码
            
        Returns:
            tuple: (响应体, 状态码)
        """
        response = {
            'success': False,
            'error': error
        }
        
        if details:
            response['details'] = details
            
        return jsonify(response), status_code
    
    @staticmethod
    def validation_error(error: str, details: str = None) -> tuple:
        """验证错误响应
        
        Args:
            error: 错误消息
            details: 错误详情
            
        Returns:
            tuple: (响应体, 状态码)
        """
        return APIResponse.error(error, details, 400)
    
    @staticmethod
    def not_found(resource: str = "Resource") -> tuple:
        """资源未找到响应
        
        Args:
            resource: 资源名称
            
        Returns:
            tuple: (响应体, 状态码)
        """
        return APIResponse.error(f"{resource} not found", status_code=404)
    
    @staticmethod
    def unauthorized(message: str = "Unauthorized access") -> tuple:
        """未授权响应
        
        Args:
            message: 错误消息
            
        Returns:
            tuple: (响应体, 状态码)
        """
        return APIResponse.error(message, status_code=401)
    
    @staticmethod
    def forbidden(message: str = "Access forbidden") -> tuple:
        """禁止访问响应
        
        Args:
            message: 错误消息
            
        Returns:
            tuple: (响应体, 状态码)
        """
        return APIResponse.error(message, status_code=403)