with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
import re
count = 0
for i, line in enumerate(lines):
    if re.search(r'el\.style|statusEl|\.style|\.display|\.height', line):
        print(f"{i+1}:{line.rstrip()}")
        count += 1
        if count >= 40: break
