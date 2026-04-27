import os

directory = '.'

for filename in os.listdir(directory):
    if not filename.endswith('.html'):
        continue
        
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r') as f:
        content = f.read()

    target = ".info-col { border-right: none !important; border-bottom: 1px solid var(--line) !important; padding: 40px 24px !important; }"
    replacement = target + "\n      .info-col:last-child { border-bottom: none !important; }"
    
    # We want to replace it only if the replacement isn't already there
    if target in content and replacement not in content:
        new_content = content.replace(target, replacement)
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed double line CSS in {filename}")

