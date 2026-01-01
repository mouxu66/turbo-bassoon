from app import app
from io import BytesIO
import sys

print("=== 直接测试路由处理 ===")

test_cases = [
    ('/', 'GET', '主页'),
    ('/about', 'GET', '关于页面'),
    ('/analysis', 'GET', '分析页面'),
    ('/items', 'GET', '装备页面'),
    ('/upload', 'GET', '上传页面'),
    ('/match_analysis', 'GET', '比赛分析'),
    ('/match_results', 'GET', '比赛结果')
]

# 模拟WSGI环境测试
def test_path(path, method='GET'):
    environ = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'SERVER_NAME': 'localhost',
        'SERVER_PORT': '80',
        'wsgi.url_scheme': 'http'
    }
    
    response_data = BytesIO()
    
    def start_response(status, headers):
        response_data.write(f"Status: {status}\\n".encode())
        for header, value in headers:
            response_data.write(f"{header}: {value}\\n".encode())
        response_data.write(b"\\n")
        return lambda data: response_data.write(data)
    
    try:
        result = app(environ, start_response)
        for data in result:
            if data:
                response_data.write(data)
        
        response_str = response_data.getvalue().decode('utf-8', errors='ignore')
        status_line = response_str.split('\\n')[0]
        status_code = int(status_line.split(' ')[1])
        return status_code, len(response_str), response_str[:200]
    except Exception as e:
        return 0, 0, f"异常: {e}"

for path, method, name in test_cases:
    status, length, preview = test_path(path, method)
    
    if status == 200:
        print(f"✅ {name:10} {path:20} 状态: {status}, 长度: {length}字节")
    elif status == 404:
        print(f"❌ {name:10} {path:20} 状态: {status} (路由可能不匹配)")
        # 检查路由匹配
        with app.test_request_context(path):
            try:
                match = app.url_map.bind('localhost').match(path)
                print(f"     但路由匹配到: {match}")
            except Exception as e:
                print(f"     路由匹配失败: {e}")
    elif status == 500:
        print(f"⚠️  {name:10} {path:20} 状态: {status} (服务器内部错误)")
        print(f"     预览: {preview}")
    else:
        print(f"❓ {name:10} {path:20} 状态: {status}, 预览: {preview[:100]}")
