import os

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 修复常见的模板语法错误
    # 1. 移除错误的单引号转义
    content = content.replace("\\'", "'")
    # 2. 修复 url_for 语法
    content = content.replace("{{ url_for(\\'", "{{ url_for('")
    content = content.replace("\\') }}", "') }}")
    
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"已修复: {filepath}")

# 修复这两个文件
for file in ['templates/about.html', 'templates/analysis.html']:
    if os.path.exists(file):
        fix_file(file)
