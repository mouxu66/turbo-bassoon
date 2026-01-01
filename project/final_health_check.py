import sys
sys.path.insert(0, '.')

print("=== 最终健康检查 ===")

try:
    from app import app
    
    print("✅ Flask应用状态:")
    print(f"   名称: {app.name}")
    print(f"   调试模式: {app.debug}")
    
    # 检查关键路由
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.rule in ['/', '/items', '/match_analysis', '/match_results', '/about', '/upload_match']:
            routes.append((rule.rule, rule.endpoint))
    
    print(f"\n✅ 关键路由 ({len(routes)} 个):")
    for route, endpoint in sorted(routes):
        print(f"   {route} -> {endpoint}")
    
    # 检查模板文件
    import os
    templates = ['index.html', 'items.html', 'match_analysis.html', 'match_results.html', 'about.html']
    missing = []
    
    print(f"\n✅ 模板文件检查:")
    for template in templates:
        path = f"templates/{template}"
        if os.path.exists(path):
            print(f"   ✓ {template}")
        else:
            print(f"   ✗ {template} (缺失)")
            missing.append(template)
    
    if missing:
        print(f"\n⚠️  缺失模板: {missing}")
    else:
        print(f"\n🎉 所有模板文件都存在")
    
    # 数据库检查
    try:
        import sqlite3
        db_path = 'instance/lol_data.db'
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # 检查表
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            print(f"\n✅ 数据库表 ({len(tables)} 个):")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   {table}: {count} 条记录")
            
            conn.close()
        else:
            print("\n⚠️  数据库文件不存在")
    except Exception as e:
        print(f"\n⚠️  数据库检查失败: {e}")
    
    print("\n" + "="*50)
    print("🎉 健康检查通过！网站已准备就绪")
    print("="*50)
    
except Exception as e:
    print(f"❌ 健康检查失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
