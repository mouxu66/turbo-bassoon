from app import app

print("=== Flask应用的路由表 ===")
print("端点(endpoint) -> 路由规则(rule)")
print("-" * 60)

# 按规则排序
rules = sorted(app.url_map.iter_rules(), key=lambda x: x.rule)

for rule in rules:
    if 'static' not in rule.endpoint:
        methods = ','.join(rule.methods - {'OPTIONS', 'HEAD'})
        print(f"{rule.endpoint:30} -> {rule.rule:30} [{methods}]")

print("\n=== 测试关键路径匹配 ===")
test_paths = ['/analysis', '/items', '/match_analysis']

for path in test_paths:
    print(f"\n测试: {path}")
    with app.test_request_context(path):
        try:
            endpoint, values = app.match_request()
            print(f"  ✅ 匹配到: {endpoint} (参数: {values})")
            
            # 检查对应的视图函数
            view_func = app.view_functions.get(endpoint)
            if view_func:
                print(f"     视图函数: {view_func.__name__}")
            else:
                print(f"     ⚠️ 端点 {endpoint} 没有对应的视图函数！")
                
        except Exception as e:
            print(f"  ❌ 匹配失败: {e}")
