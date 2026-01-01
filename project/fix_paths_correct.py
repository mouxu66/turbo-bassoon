import os
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 【关键】修正：移除错误添加的反斜杠转义，使用正确的Jinja2语法
    # 1. 修正 url_for 语法：将错误转义的单引号恢复
    # 匹配类似 {{ url_for(\'static\', filename=\'...\') }} 的错误模式
    # 并将其替换为正确的 {{ url_for('static', filename='...') }}
    content = re.sub(r"\{\{\s*url_for\\(\\'static\\',\\s*filename=\\'(.*?)\\'\\s*\)\s*\}\}", r"{{ url_for('static', filename='\1') }}", content)
    
    # 2. 同时确保路径不以斜杠开头（filename参数不应以/开头）
    # 将 filename='/assets/...' 改为 filename='assets/...'
    content = re.sub(r"filename=\\'/([^']*)\\'", r"filename='\1'", content)
    
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"已修复: {filepath}")

# 修复所有模板文件
templates_dir = 'templates'
for filename in os.listdir(templates_dir):
    if filename.endswith('.html'):
        fix_file(os.path.join(templates_dir, filename))
