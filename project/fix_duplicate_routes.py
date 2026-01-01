import re

with open('app.py', 'r') as f:
    content = f.read()

# 查找所有路由定义
pattern = r'@app\.route\([^)]+\)\s*\n\s*def (\w+)'
routes = re.findall(pattern, content)

print("找到的路由函数:")
for route in routes:
    print(f"  - {route}")

# 检查重复的 match_analysis
match_analysis_count = routes.count('match_analysis')
print(f"\nmatch_analysis 出现了 {match_analysis_count} 次")

if match_analysis_count > 1:
    print("发现重复的 match_analysis 路由，正在修复...")
    
    # 读取文件行
    with open('app.py', 'r') as f:
        lines = f.readlines()
    
    # 找到第一个 match_analysis 函数
    first_match = None
    second_match = None
    in_first_function = False
    in_second_function = False
    first_start = None
    second_start = None
    
    for i, line in enumerate(lines):
        if 'def match_analysis():' in line:
            if first_match is None:
                first_match = i
                in_first_function = True
            elif second_match is None:
                second_match = i
                in_second_function = True
                break
    
    print(f"第一个 match_analysis 在第 {first_match+1} 行")
    print(f"第二个 match_analysis 在第 {second_match+1} 行")
    
    # 建议保留第二个（我们新加的），删除第一个
    if first_match is not None and second_match is not None:
        # 找到第一个函数的路由装饰器
        for i in range(first_match-1, max(0, first_match-10), -1):
            if '@app.route' in lines[i]:
                print(f"删除第 {i+1} 行的路由装饰器")
                lines[i] = '# ' + lines[i]  # 注释掉
        
        # 注释掉第一个函数
        print(f"注释第 {first_match+1} 行的函数定义")
        lines[first_match] = '# ' + lines[first_match]
        
        # 写回文件
        with open('app.py', 'w') as f:
            f.writelines(lines)
        
        print("✅ 已注释掉旧的 match_analysis 函数")
    else:
        print("无法定位重复的函数")
else:
    print("✅ 没有重复的路由")

