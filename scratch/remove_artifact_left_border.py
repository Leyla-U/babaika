import os
import glob
import re

count = 0
for file in glob.glob('*.html'):
    with open(file, 'r') as f:
        content = f.read()
        
    # Replace border-right: 1px solid var(--line); inside .artifact-left { ... }
    # Since .artifact-left can span multiple lines, we use regex with DOTALL.
    # But wait, it might be simpler to just remove border-right: 1px solid var(--line);
    # ONLY when it's immediately after .artifact-left { or within its block.
    # Actually, let's just do it cleanly line by line if possible, or string replace if it's identical.
    
    # We saw in tamarisk.html:
    #     .artifact-left { cursor: pointer;
    #       padding: 72px 64px;
    #       border-right: 1px solid var(--line);
    #       display: flex; flex-direction: column; justify-content: flex-start;
    #     }
    
    # Let's replace the exact line if it exists in the artifact-left block context.
    # Since it's easier, we can just replace "border-right: 1px solid var(--line);" with "" 
    # IF the previous few lines contain ".artifact-left {"
    
    lines = content.split('\n')
    new_lines = []
    in_artifact_left = False
    
    for line in lines:
        if '.artifact-left {' in line or '.artifact-left' in line and '{' in line:
            in_artifact_left = True
            
        if in_artifact_left and 'border-right: 1px solid var(--line);' in line:
            line = line.replace('border-right: 1px solid var(--line);', '')
            
        if in_artifact_left and '}' in line:
            in_artifact_left = False
            
        new_lines.append(line)
        
    new_content = '\n'.join(new_lines)
    
    if new_content != content:
        with open(file, 'w') as f:
            f.write(new_content)
        count += 1
        print(f"Updated {file}")

print(f"Total files updated: {count}")
