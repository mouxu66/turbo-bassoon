import os
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 修复常见的错误链接模式
    replacements = [
        # 静态 .html 文件链接 -> Flask路由
        (r'href="about\.html"', 'href="{{ url_for(\'about\') }}"'),
        (r'href="analysis\.html"', 'href="{{ url_for(\'analysis\') }}"'),
        (r'href="items\.html"', 'href="{{ url_for(\'items_page\') }}"'),
        (r'href="upload\.html"', 'href="{{ url_for(\'upload_page\') }}"'),
        (r'href="match_analysis\.html"', 'href="{{ url_for(\'match_analysis\') }}"'),
        (r'href="match_results\.html"', 'href="{{ url_for(\'match_results\') }}"'),
        
        # 错误的路径前缀
        (r'href="/docs/about"', 'href="{{ url_for(\'about\') }}"'),
        (r'href="/docs/analysis"', 'href="{{ url_for(\'analysis\') }}"'),
        (r'href="/page/about"', 'href="{{ url_for(\'about\') }}"'),
        
        # 绝对路径但错误的
        (r'href="/about.html"', 'href="{{ url_for(\'about\') }}"'),
        (r'href="/analysis.html"', 'href="{{ url_for(\'analysis\') }}"'),
    ]
    
    changed = False
    for pattern, replacement in replacements:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            changed = True
            print(f"  修复: {pattern} -> {replacement}")
    
    if changed:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

print("修复网站内部链接...")
fixed_files = []
for filename in os.listdir('templates'):
    if filename.endswith('.html'):
        filepath = os.path.join('templates', filename)
        print(f"检查: {filename}")
        if fix_file(filepath):
            fixed_files.append(filename)

if fixed_files:
    print(f"\n✅ 已修复以下文件的链接: {', '.join(fixed_files)}")
else:
    print("\n✅ 未发现需要修复的链接")
