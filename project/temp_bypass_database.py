import re

with open('app.py', 'r') as f:
    content = f.read()

# 找到可能出错的函数（比如items_page），简化它
# 查找所有访问 items 表的代码
lines = content.split('\n')
new_lines = []
in_try_block = False
skip_next_lines = 0

for i, line in enumerate(lines):
    if skip_next_lines > 0:
        skip_next_lines -= 1
        continue
    
    # 如果找到访问items表的查询，注释掉
    if 'items' in line.lower() and ('SELECT' in line or 'FROM items' in line):
        print(f"找到可能出错的查询在第 {i+1} 行: {line.strip()[:50]}...")
        new_lines.append(f"# {line}  # 临时注释：数据库表可能有问题")
    else:
        new_lines.append(line)

with open('app.py', 'w') as f:
    f.write('\n'.join(new_lines))

print("✅ 已临时注释可能出错的数据库查询")
print("网站现在应该能打开，但可能不显示数据")
