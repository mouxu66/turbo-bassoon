with open('templates/match_analysis.html', 'r') as f:
    content = f.read()

# 统计 block title 出现的次数
count = content.count('{% block title %}')
print(f"找到 {count} 处 'block title' 定义")

if count > 1:
    # 替换：只保留第一个，删除后续的
    parts = content.split('{% block title %}', 1)
    first_part = parts[0]
    rest = parts[1]
    
    # 在剩余部分中删除额外的 block title
    rest = rest.replace('{% block title %}', '', 1)
    
    content = first_part + '{% block title %}' + rest
    
    with open('templates/match_analysis.html', 'w') as f:
        f.write(content)
    print("✅ 已修复重复的 block title")
else:
    print("✅ 没有发现重复定义")
