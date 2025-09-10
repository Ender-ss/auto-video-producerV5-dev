import os
import re

# Procurar por padrões que podem estar causando o problema
patterns = [
    r'\.fadein\(',
    r'\.fadeout\(',
    r'\.resize\(',
    r'\.fx\(',
    r'clip\.fadein',
    r'clip\.fadeout',
    r'clip\.resize'
]

found = []

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.py') and 'site-packages' not in root:
            try:
                with open(os.path.join(root, f), 'r', encoding='utf-8', errors='ignore') as file:
                    lines = file.readlines()
                    for i, line in enumerate(lines):
                        for pattern in patterns:
                            if re.search(pattern, line):
                                found.append((os.path.join(root, f), i+1, line.strip(), pattern))
            except:
                pass

for file, line, content, pattern in found[:30]:
    print(f'{file}:{line} [{pattern}]: {content}')

print(f'\nTotal encontrado: {len(found)} ocorrências')