import os
import re

def fix_content(content):
    # Target elements that have both borders in style attribute
    # Example: style="...border-top: 1px solid var(--line);...border-bottom: 1px solid var(--line);..."
    
    # regex to find style attributes containing both
    pattern = re.compile(r'(style="[^"]*)\s*border-top:\s*1px\s*solid\s*var\(--line\);\s*([^"]*border-bottom:\s*1px\s*solid\s*var\(--line\);[^"]*")', re.IGNORECASE)
    content = pattern.sub(r'\1\2', content)
    
    # Handle the reverse order just in case
    pattern2 = re.compile(r'(style="[^"]*)\s*border-bottom:\s*1px\s*solid\s*var\(--line\);\s*([^"]*border-top:\s*1px\s*solid\s*var\(--line\);[^"]*")', re.IGNORECASE)
    content = pattern2.sub(r'\1\2', content)
    
    # Also specifically target "border-top: none;" placeholders if any exist from previous edits and remove them for cleanliness
    content = content.replace('border-top: none;', '')
    content = content.replace('border-bottom: none;', '')
    
    # Remove any empty or trailing spaces/semicolons left behind in style
    content = re.sub(r'style="\s*;?\s*"', '', content)
    
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
                        print(f"Deep clean: {path}")
                except Exception as e:
                    print(f"Error {path}: {e}")

if __name__ == "__main__":
    main()
