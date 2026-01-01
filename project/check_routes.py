from app import app

print("=== 当前注册的所有路由 ===")
for rule in app.url_map.iter_rules():
    if 'static' not in rule.endpoint and 'api' not in rule.endpoint:
        print(f"{rule.rule:<25} -> {rule.endpoint}")

print("\n=== 你需要但可能缺失的路由 ===")
required_routes = ['/about', '/analysis', '/items', '/upload', '/match_analysis', '/match_results']
for route in required_routes:
    found = any(rule.rule == route for rule in app.url_map.iter_rules())
    status = "✅ 已存在" if found else "❌ 缺失"
    print(f"{route:<25} {status}")
