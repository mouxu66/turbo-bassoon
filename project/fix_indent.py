import re

with open('app.py', 'r') as f:
    lines = f.readlines()

print(f"总行数: {len(lines)}")

# 检查540-570行
problem_start = None
for i in range(539, 570):  # Python索引从0开始
    if i < len(lines):
        line = lines[i]
        # 检查是否有不正确的缩进
        if line.strip() and not line.startswith(' ') and not line.startswith('@') and not line.startswith('def') and not line.startswith('#'):
            print(f"第{i+1}行可能有缩进问题: {repr(line)}")
            if problem_start is None:
                problem_start = i

if problem_start:
    print(f"\n从第{problem_start+1}行开始修复...")
    
    # 找到这个函数的开始
    func_start = None
    for i in range(problem_start, max(0, problem_start-20), -1):
        if i < len(lines) and lines[i].strip().startswith('def '):
            func_start = i
            break
    
    if func_start:
        print(f"函数从第{func_start+1}行开始: {lines[func_start].strip()}")
        
        # 检查函数体缩进
        for i in range(func_start+1, min(func_start+30, len(lines))):
            if lines[i].strip() and not lines[i].startswith('    '):
                # 修复缩进
                lines[i] = '    ' + lines[i].lstrip()
                print(f"修复第{i+1}行缩进")
    
    # 写回文件
    with open('app.py', 'w') as f:
        f.writelines(lines)
    
    print("✅ 缩进修复完成")
else:
    print("✅ 没有发现明显的缩进问题")
