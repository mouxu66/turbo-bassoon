from app import app
import re

print("=== 完整网站导航测试 ===\n")

with app.test_client() as client:
    # 测试从主页开始完整导航
    print("1. 访问主页...")
    home_response = client.get('/')
    assert home_response.status_code == 200
    print("   ✅ 主页可访问")
    
    # 从主页提取所有导航链接
    home_html = home_response.get_data(as_text=True)
    
    # 查找导航菜单中的链接（通常是nav, navbar, menu类）
    nav_links = []
    lines = home_html.split('\n')
    for i, line in enumerate(lines):
        if 'nav-link' in line or 'navbar' in line or 'menu' in line:
            # 提取href
            href_match = re.search(r'href="([^"]*)"', line)
            if href_match:
                href = href_match.group(1)
                if href.startswith('/') and 'static' not in href:
                    # 获取链接文本（下一行或当前行）
                    text = line.strip()
                    if i+1 < len(lines):
                        next_line = lines[i+1]
                        if '>' in next_line and '</a>' not in next_line:
                            text = next_line.strip()
                    
                    nav_links.append((href, text[:30]))
    
    print(f"\n2. 找到 {len(nav_links)} 个导航链接:")
    
    # 测试每个导航链接
    for href, text in sorted(set(nav_links)):
        if href == '/':
            continue
            
        try:
            response = client.get(href)
            if response.status_code == 200:
                print(f"   ✅ {href:20} -> 可访问 ({text}...)")
                
                # 检查这个页面中的返回链接
                page_html = response.get_data(as_text=True)
                if 'href="/"' in page_html:
                    print(f"        ↳ 有返回主页链接")
                    
            elif response.status_code == 404:
                print(f"   ❌ {href:20} -> 404 NOT FOUND")
            else:
                print(f"   ⚠️  {href:20} -> 状态码 {response.status_code}")
                
        except Exception as e:
            print(f"   💥 {href:20} -> 异常: {str(e)[:30]}")
    
    print("\n3. 测试完整用户流程:")
    print("   🏠 主页 -> 📦 装备库 -> 📊 数据分析 -> ℹ️ 关于 -> 🏠 主页")
    
    # 模拟用户点击流程
    flow = ['/', '/items', '/analysis', '/about', '/']
    for i, path in enumerate(flow):
        response = client.get(path)
        status = "✅" if response.status_code == 200 else "❌"
        page_name = {
            '/': '主页',
            '/items': '装备库', 
            '/analysis': '数据分析',
            '/about': '关于页面'
        }.get(path, path)
        
        print(f"   {status} 步骤{i+1}: {path:15} ({page_name})")
    
    print("\n🎉 导航测试完成！")
