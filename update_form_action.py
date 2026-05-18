import os
import glob

html_files = glob.glob('/Users/leylaudimamedova/babaika/*.html')
updated_count = 0

old_action = 'action="https://formspree.io/f/YOUR_FORM_ID"'
new_action = 'action="/api/contact"'

for filepath in html_files:
    with open(filepath, 'r') as f:
        content = f.read()
        
    if old_action in content:
        content = content.replace(old_action, new_action)
        with open(filepath, 'w') as f:
            f.write(content)
        updated_count += 1
        print(f"Updated {os.path.basename(filepath)}")

print(f"Total updated: {updated_count}")
