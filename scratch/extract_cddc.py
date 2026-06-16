import json
import re

with open('frontend/src/services/demo-ele203-0237ictve-curso202526.ts', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('"0237-ictve-curso-2025-26": {')
if start == -1:
    print('Not found')
    exit(1)

start = text.find('{', start)
stack = 0
end = -1
for i in range(start, len(text)):
    if text[i] == '{':
        stack += 1
    elif text[i] == '}':
        stack -= 1
        if stack == 0:
            end = i + 1
            break

json_str = text[start:end]
try:
    data = json.loads(json_str)
    data['__version__'] = 1
    with open('0552-sirl-curso-2025-26.cddc', 'w', encoding='utf-8') as out:
        json.dump(data, out, ensure_ascii=False, indent=2)
    print('Generated 0552-sirl-curso-2025-26.cddc')
except Exception as e:
    print('Error:', e)
