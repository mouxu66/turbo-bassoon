import os
import re

def fix_template_file(filepath):
    """修复模板文件中的语法错误"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复常见的Jinja2语法错误
    fixes = [
        # 修复反斜杠转义的单引号
        (r"url_for\\(\\\\'", "url_for('"),
        (r"url_for\\(\\'", "url_for('"),
        (r"url_for\\(\"", "url_for('"),
        # 修复结束括号
        (r"\\')", "')"),
        (r'\\")', "')"),
        # 修复多余的转义
        (r"\\\\", ""),
    ]
    
    original = content
    for pattern, replacement in fixes:
        content = re.sub(pattern, replacement, content)
    
    if original != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 修复: {filepath}")
        return True
    return False

# 修复所有HTML模板
fixed_count = 0
for root, dirs, files in os.walk('templates'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            if fix_template_file(filepath):
                fixed_count += 1

print(f"\n🎉 修复了 {fixed_count} 个模板文件")
