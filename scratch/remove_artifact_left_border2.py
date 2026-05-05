import os
import glob
import re

count = 0
for file in glob.glob('*.html'):
    with open(file, 'r') as f:
        content = f.read()
        
    # We want to remove "border-right: 1px solid var(--line);" from anywhere inside the 
    # .artifact-left block in CSS.
    # The safest way is to use regex: replace the specific line.
    
    new_content = re.sub(
        r'(\.artifact-left\s*\{[^}]*)border-right:\s*1px\s*solid\s*var\(--line\);(.*?\})',
        r'\1\2',
        content,
        flags=re.DOTALL
    )
    
    if new_content != content:
        with open(file, 'w') as f:
            f.write(new_content)
        count += 1
        print(f"Updated {file}")

print(f"Total files updated: {count}")
