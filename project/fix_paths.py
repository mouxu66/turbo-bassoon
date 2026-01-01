import os
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 替换CSS链接
    content = re.sub(r'href="([^"]*\.css)"', r'href="{{ url_for(\'static\', filename=\'\1\') }}"', content)
    # 替换JS脚本
    content = re.sub(r'src="([^"]*\.js)"', r'src="{{ url_for(\'static\', filename=\'\1\') }}"', content)
    # 替换图片（常见格式）
    content = re.sub(r'src="([^"]*\.(?:png|jpg|jpeg|gif|svg|ico))"', r'src="{{ url_for(\'static\', filename=\'\1\') }}"', content)
    
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"已修复: {filepath}")

# 修复所有模板文件
templates_dir = 'templates'
for filename in os.listdir(templates_dir):
    if filename.endswith('.html'):
        fix_file(os.path.join(templates_dir, filename))
