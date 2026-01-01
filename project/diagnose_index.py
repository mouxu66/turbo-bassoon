import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"文件总行数: {len(lines)}")

# 检查第228行
if len(lines) >= 228:
    line_228 = lines[227]
    print(f"\n第228行内容: {repr(line_228)}")
    
    # 检查反斜杠
    if '\\' in line_228:
        print("⚠️  发现反斜杠字符:")
        for i, char in enumerate(line_228):
            if char == '\\':
                print(f"  位置 {i}: 反斜杠")
    
    # 检查Jinja2语法
    jinja_patterns = [r'\{\{.*?\}\}', r'\{\%.*?\%\}']
    for pattern in jinja_patterns:
        matches = re.findall(pattern, line_228)
        if matches:
            print(f"Jinja2语法: {matches}")

# 检查上下文
print(f"\n第220-235行:")
for i in range(219, min(235, len(lines))):
    line_num = i + 1
    line = lines[i].rstrip()
    print(f"{line_num:3}: {line[:80]}{'...' if len(line) > 80 else ''}")

# 检查是否有语法错误
print(f"\n=== 检查Jinja2语法错误 ===")
for i, line in enumerate(lines):
    line_num = i + 1
    # 检查未闭合的{{ }}
    if '{{' in line and '}}' not in line:
        # 检查下一行是否有}}
        next_line = lines[i+1] if i+1 < len(lines) else ''
        if '}}' not in next_line:
            print(f"⚠️  第{line_num}行: 可能未闭合的{{ }}")
            print(f"   内容: {line.rstrip()}")
    
    # 检查未闭合的{% %}
    if '{%' in line and '%}' not in line:
        next_line = lines[i+1] if i+1 < len(lines) else ''
        if '%}' not in next_line:
            print(f"⚠️  第{line_num}行: 可能未闭合的{{% %}}")
            print(f"   内容: {line.rstrip()}")
