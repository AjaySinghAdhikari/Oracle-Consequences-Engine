with open('frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
import re
matches = re.finditer(r'\[([^\]]+)\]\(http[^\)]+\)', content)
for m in matches:
    line_num = content[:m.start()].count('\n') + 1
    print(f'Line {line_num}: {repr(m.group())}')
