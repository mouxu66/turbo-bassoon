from app import app
import requests
from werkzeug.serving import make_server
import threading
import time

# 启动一个临时测试服务器
def run_test_server():
    server = make_server('localhost', 8765, app)
    server.serve_forever()

# 在后台启动服务器
thread = threading.Thread(target=run_test_server, daemon=True)
thread.start()
time.sleep(2)  # 等待服务器启动

# 测试实际请求
print("=== 模拟真实浏览器请求测试 ===")
url_base = "http://localhost:8765"

test_pages = [
    ('/', '主页'),
    ('/about', '关于'),
    ('/analysis', '分析'),
    ('/items', '装备'),
    ('/upload', '上传'),
    ('/match_analysis', '比赛分析'),
    ('/match_results', '比赛结果')
]

for path, name in test_pages:
    try:
        response = requests.get(url_base + path, timeout=5)
        status = "✅" if response.status_code == 200 else f"❌ {response.status_code}"
        print(f"{name:8} {path:20} {status} (长度: {len(response.content)}字节)")
        
        if response.status_code != 200:
            print(f"      响应预览: {response.text[:100]}")
    except Exception as e:
        print(f"{name:8} {path:20} ❌ 请求失败: {e}")

print("\n=== 检查路由匹配 ===")
with app.test_request_context():
    for path, name in test_pages:
        try:
            match = app.url_map.bind('localhost').match(path)
            print(f"{name:8} {path:20} ✅ 路由匹配: {match}")
        except Exception as e:
            print(f"{name:8} {path:20} ❌ 路由不匹配: {e}")
