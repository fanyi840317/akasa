import unittest
import json
from flask import Flask
from api.response import APIResponse


class TestAPIResponse(unittest.TestCase):
    """测试APIResponse统一响应类"""
    
    def setUp(self):
        """设置测试环境"""
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """清理测试环境"""
        self.app_context.pop()
    
    def test_success_response_with_data(self):
        """测试成功响应包含数据"""
        test_data = {'key': 'value', 'number': 123}
        response, status_code = APIResponse.success(data=test_data)
        
        self.assertEqual(status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['data'], test_data)
        self.assertNotIn('message', response_data)
    
    def test_success_response_with_message(self):
        """测试成功响应包含消息"""
        test_message = 'Operation completed successfully'
        response, status_code = APIResponse.success(message=test_message)
        
        self.assertEqual(status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], test_message)
        self.assertNotIn('data', response_data)
    
    def test_success_response_with_data_and_message(self):
        """测试成功响应同时包含数据和消息"""
        test_data = {'items': [1, 2, 3]}
        test_message = 'Data retrieved successfully'
        response, status_code = APIResponse.success(data=test_data, message=test_message)
        
        self.assertEqual(status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['data'], test_data)
        self.assertEqual(response_data['message'], test_message)
    
    def test_error_response_basic(self):
        """测试基本错误响应"""
        error_message = 'Something went wrong'
        response, status_code = APIResponse.error(error_message)
        
        self.assertEqual(status_code, 500)
        response_data = json.loads(response.get_data(as_text=True))
        
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['error'], error_message)
        self.assertNotIn('details', response_data)
    
    def test_error_response_with_details(self):
        """测试包含详情的错误响应"""
        error_message = 'Validation failed'
        error_details = 'Field "name" is required'
        response, status_code = APIResponse.error(error_message, details=error_details)
        
        self.assertEqual(status_code, 500)
        response_data = json.loads(response.get_data(as_text=True))
        
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['error'], error_message)
        self.assertEqual(response_data['details'], error_details)
    
    def test_error_response_custom_status_code(self):
        """测试自定义状态码的错误响应"""
        error_message = 'Bad request'
        response, status_code = APIResponse.error(error_message, status_code=400)
        
        self.assertEqual(status_code, 400)
        response_data = json.loads(response.get_data(as_text=True))
        
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['error'], error_message)
    
    def test_validation_error_response(self):
        """测试验证错误响应"""
        error_message = 'Invalid input'
        error_details = 'Email format is incorrect'
        response, status_code = APIResponse.validation_error(error_message, details=error_details)
        
        self.assertEqual(status_code, 400)
        response_data = json.loads(response.get_data(as_text=True))
        
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['error'], error_message)
        self.assertEqual(response_data['details'], error_details)
    
    def test_not_found_response(self):
        """测试资源未找到响应"""
        resource_name = 'User'
        response, status_code = APIResponse.not_found(resource_name)
        
        self.assertEqual(status_code, 404)
        response_data = json.loads(response.get_data(as_text=True))
        
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['error'], f'{resource_name} not found')
    
    def test_unauthorized_response(self):
        """测试未授权响应"""
        response, status_code = APIResponse.unauthorized()
        
        self.assertEqual(status_code, 401)
        response_data = json.loads(response.get_data(as_text=True))
        
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['error'], 'Unauthorized access')
    
    def test_forbidden_response(self):
        """测试禁止访问响应"""
        custom_message = 'Insufficient permissions'
        response, status_code = APIResponse.forbidden(custom_message)
        
        self.assertEqual(status_code, 403)
        response_data = json.loads(response.get_data(as_text=True))
        
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['error'], custom_message)


if __name__ == '__main__':
    unittest.main()