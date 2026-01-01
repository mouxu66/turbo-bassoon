import os
import re

print("=== 批量修复所有文件中的错误链接 ===")

files_to_fix = ['about.html', 'analysis.html', 'items.html']
fixed_count = 0

for filename in files_to_fix:
    filepath = os.path.join('templates', filename)
    
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在: {filename}")
        continue
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 统计修复前
    count_before = content.count('href="/items.html"')
    
    if count_before > 0:
        # 修复1: /items.html -> /items
        content = content.replace('href="/items.html"', 'href="/items"')
        
        # 修复2: items.html (无斜杠) -> /items
        content = content.replace('href="items.html"', 'href="/items"')
        
        count_after = content.count('items.html')
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"✅ {filename}: 修复了 {count_before} 处链接")
        fixed_count += 1
    else:
        print(f"✅ {filename}: 无需修复")

print(f"\n总计修复了 {fixed_count} 个文件")

# 验证修复
print("\n=== 验证修复结果 ===")
for filename in files_to_fix:
    filepath = os.path.join('templates', filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        remaining = content.count('items.html')
        status = "✅" if remaining == 0 else f"❌ 仍有 {remaining} 处"
        print(f"{filename:20} {status}")
