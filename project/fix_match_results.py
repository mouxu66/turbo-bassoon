with open('templates/match_results.html', 'r') as f:
    lines = f.readlines()

# 找到第一个 block title 的位置
first_found = False
new_lines = []
for line in lines:
    if '{% block title %}' in line:
        if not first_found:
            new_lines.append(line)  # 保留第一个
            first_found = True
        # 跳过后续的 block title
    else:
        new_lines.append(line)

with open('templates/match_results.html', 'w') as f:
    f.writelines(new_lines)
print("✅ 已修复 match_results.html 的重复 block title")
