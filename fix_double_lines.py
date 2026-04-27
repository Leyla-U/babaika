import os
import re

def fix_content(content):
    # 1. Remove border-top from info-band that has both top and bottom
    # Pattern: <div class="info-band reveal" style="border-top: 1px solid var(--line); border-bottom: 1px solid var(--line);">
    content = re.sub(
        r'(<div class="info-band reveal" style=")\s*border-top: 1px solid var\(--line\);\s*(border-bottom: 1px solid var\(--line\);")',
        r'\1\2',
        content
    )
    
    # 2. Remove border-top from the navigation div (Next Chapter / Explore)
    # Pattern: <div style="display: flex; justify-content: center; padding: 120px 24px 60px; border-top: 1px solid var(--line);">
    # We'll also change it to border-bottom to separate from footer if needed, but the user asked to clean up double lines.
    # Actually, most artifacts already have border-bottom.
    content = re.sub(
        r'(<div style="display: flex; justify-content: center; padding: 120px 24px 60px;)\s*border-top: 1px solid var\(--line\);',
        r'\1',
        content
    )
    
    # Also handle variants with different padding or flex properties
    content = re.sub(
        r'(<div class="info-band reveal" style="border-top: none;)\s*border-bottom: 1px solid var\(--line\);',
        r'<div class="info-band reveal" style="border-bottom: 1px solid var(--line);',
        content
    )
    
    return content

def main():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = fix_content(content)
                    
                    if new_content != content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Fixed: {path}")
                except Exception as e:
                    print(f"Error {path}: {e}")

if __name__ == "__main__":
    main()
