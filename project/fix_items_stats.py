with open('app.py', 'r') as f:
    lines = f.readlines()

# 查找 items_page 函数中的 matches 表查询
in_items_func = False
for i, line in enumerate(lines):
    if 'def items_page' in line:
        in_items_func = True
    if in_items_func and 'def ' in line and 'items_page' not in line:
        in_items_func = False
    
    if in_items_func and 'matches' in line and 'SELECT' in line:
        print(f"找到问题行 {i+1}: {line.strip()}")
        # 注释掉这行
        lines[i] = '# ' + line
        print("已注释该查询")

with open('app.py', 'w') as f:
    f.writelines(lines)
print("✅ 已临时修复 items 页面的统计查询")
