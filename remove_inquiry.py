import os
import re

directory = '.'

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as f:
            content = f.read()

        # Regex to match the Inquiry button
        # It looks like: <button class="btn-buy-now btn-glass" ...>Inquire</button>
        # or similar variants.
        new_content = re.sub(r'<button[^>]*class="[^"]*btn-buy-now[^"]*"[^>]*>Inquire</button>\s*', '', content, flags=re.IGNORECASE)
        
        # In build_pages.rb (not HTML but we might want to clean up)
        if content != new_content:
            with open(filepath, 'w') as f:
                f.write(new_content)
            print(f"Removed Inquiry button from {filename}")

