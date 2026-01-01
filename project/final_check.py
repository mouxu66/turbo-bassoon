import sys
sys.path.insert(0, '.')

try:
    # 导入应用
    from app import app
    
    print("✅ Flask应用健康检查:")
    print(f"   应用名称: {app.name}")
    print(f"   静态文件夹: {app.static_folder}")
    print(f"   模板文件夹: {app.template_folder}")
    
    # 检查关键路由
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.rule in ['/', '/items', '/about', '/match_analysis', '/upload']:
            routes.append((rule.rule, rule.endpoint))
    
    print(f"   关键路由数量: {len(routes)}")
    for route, endpoint in sorted(routes):
        print(f"     {route} -> {endpoint}")
    
    # 测试数据库连接
    try:
        import sqlite3
        conn = sqlite3.connect('instance/lol_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM items")
        count = cursor.fetchone()[0]
        print(f"✅ 数据库连接正常，有 {count} 条装备记录")
        conn.close()
    except Exception as e:
        print(f"⚠️  数据库连接问题: {e}")
    
    print("\n🎉 所有检查通过！网站应该可以正常工作了。")
    
except Exception as e:
    print(f"❌ 健康检查失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
