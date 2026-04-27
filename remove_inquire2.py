import os
import re

directory = '.'

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as f:
            content = f.read()

        new_content = re.sub(r'<button[^>]*class="[^"]*btn-glass[^"]*"[^>]*>Inquire</button>\s*', '', content, flags=re.IGNORECASE)
        
        if content != new_content:
            with open(filepath, 'w') as f:
                f.write(new_content)
            print(f"Removed Inquire button from {filename}")

