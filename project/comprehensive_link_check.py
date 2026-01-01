import os
import re

print("=== 全面链接检查 ===")

# 常见的错误链接模式
error_patterns = [
    r'href="[^"]*\.html"',      # 静态HTML文件
    r'href="[^"]*/docs/[^"]*"', # 旧的/docs/路径
    r'href="[^"]*/page/[^"]*"', # 旧的/page/路径
    r'src="[^"]*\.html"',       # 错误的src属性
]

for filename in os.listdir('templates'):
    if not filename.endswith('.html'):
        continue
    
    filepath = os.path.join('templates', filename)
    with open(filepath, 'r') as f:
        content = f.read()
    
    issues = []
    for pattern in error_patterns:
        matches = re.findall(pattern, content)
        if matches:
            unique_matches = list(set(matches))[:3]  # 只显示前3个不同的
            issues.append(f"{pattern}: {', '.join(unique_matches)}")
    
    if issues:
        print(f"⚠️  {filename}:")
        for issue in issues:
            print(f"    {issue}")
    else:
        print(f"✅  {filename}: 无问题链接")
