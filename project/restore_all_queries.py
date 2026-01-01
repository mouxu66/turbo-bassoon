with open('app.py', 'r') as f:
    content = f.read()

print("恢复所有被注释的数据库查询...")

# 恢复所有被我们注释掉的查询
import re

# 恢复各种格式的注释
replacements = [
    (r'# cursor\.execute\("SELECT COUNT\(\*\) FROM items"\)\s*# 临时注释：数据库表可能有问题', 
     'cursor.execute("SELECT COUNT(*) FROM items")'),
    
    (r'# SELECT \* FROM items\s*# 临时注释：数据库表可能有问题',
     'SELECT * FROM items'),
    
    (r'#\s*cursor\.execute.*FROM items.*# 临时注释',
     lambda m: m.group(0).replace('# ', '').replace('  # 临时注释', '')),
]

original = content
for pattern, replacement in replacements:
    if callable(replacement):
        content = re.sub(pattern, replacement, content)
    else:
        content = content.replace(pattern, replacement)

# 统计恢复了多少处
restored = 0
for line in content.split('\n'):
    if 'FROM items' in line and 'SELECT' in line and not line.strip().startswith('#'):
        restored += 1

with open('app.py', 'w') as f:
    f.write(content)

print(f"✅ 已恢复 {restored} 处数据库查询")
print("现在网站将正常查询数据库显示数据")
