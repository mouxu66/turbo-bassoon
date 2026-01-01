from app import app
import sys

# 禁用某些可能失败的操作
app.config['TESTING'] = True

with app.test_client() as client:
    routes_to_test = [
        ('/', '主页'),
        ('/about', '关于页面'),
        ('/analysis', '分析页面'),
        ('/items', '装备页面'),
        ('/upload', '上传页面'),
        ('/match_analysis', '比赛分析'),
        ('/match_results', '比赛结果')
    ]
    
    print("测试路由访问状态:")
    print("-" * 50)
    
    all_ok = True
    for path, desc in routes_to_test:
        try:
            response = client.get(path)
            status = "✅" if response.status_code == 200 else f"❌ {response.status_code}"
            print(f"{desc:15} {path:20} {status}")
            
            if response.status_code != 200:
                all_ok = False
                # 尝试获取错误信息
                if response.status_code == 500:
                    print(f"  错误: 500 Internal Server Error")
                elif response.status_code == 404:
                    print(f"  错误: 404 Not Found (但路由已注册)")
                    
        except Exception as e:
            print(f"{desc:15} {path:20} ❌ 异常: {str(e)[:50]}")
            all_ok = False
    
    print("-" * 50)
    if all_ok:
        print("✅ 所有路由测试通过")
    else:
        print("❌ 部分路由存在问题")
