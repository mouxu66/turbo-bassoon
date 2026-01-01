from app import app

print("=== 最终路由验证 ===")

# 正确的测试方法
with app.test_client() as client:
    test_paths = [
        ('/', '主页'),
        ('/about', '关于'),
        ('/analysis', '分析'),
        ('/items', '装备'),
        ('/upload', '上传'),
        ('/match_analysis', '比赛分析'),
        ('/match_results', '比赛结果')
    ]
    
    for path, name in test_paths:
        try:
            response = client.get(path)
            status_icon = "✅" if response.status_code == 200 else "❌"
            print(f"{status_icon} {name:8} {path:20} 状态: {response.status_code}")
            
            if response.status_code != 200:
                print(f"      响应类型: {response.content_type}")
                print(f"      内容长度: {len(response.data)} 字节")
        except Exception as e:
            print(f"❌ {name:8} {path:20} 异常: {str(e)[:50]}")

print("\n=== 路由端点映射验证 ===")
# 验证每个路由映射到不同的端点
from flask import Flask
import werkzeug.routing

test_app = Flask(__name__)
with test_app.test_request_context():
    adapter = app.url_map.bind('localhost')
    
for path, name in test_paths:
    try:
        endpoint, values = adapter.match(path)
        print(f"✅ {name:8} {path:20} -> 端点: {endpoint}")
    except werkzeug.routing.RequestRedirect as e:
        print(f"↪️ {name:8} {path:20} -> 重定向到: {e.new_url}")
    except Exception as e:
        print(f"❌ {name:8} {path:20} -> 匹配失败: {type(e).__name__}")
