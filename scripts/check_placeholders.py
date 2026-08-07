#!/usr/bin/env python3
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
patterns=[r'YOUR_USERNAME',r'TODO(?:\b|:)',r'example\.com/your',r'Lorem ipsum']
errors=[]
for p in ROOT.rglob('*'):
    if p.is_file() and '.git' not in p.parts and p.suffix in {'.md','.yml','.yaml','.json','.toml','.txt'}:
        text=p.read_text(encoding='utf-8',errors='ignore')
        for pat in patterns:
            if re.search(pat,text,re.I): errors.append(f'{p.relative_to(ROOT)} matches {pat}')
if errors: print('\n'.join(errors)); sys.exit(1)
print('PASS: no unresolved placeholders')
