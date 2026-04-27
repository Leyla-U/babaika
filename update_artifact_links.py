import os
import re

files = ["tuman.html", "tamarisk.html", "poloi.html", "il.html", "raskaty.html", "kamish.html", "cheshuya.html"]
base_path = "/Users/leylaudimamedova/babaika"

for filename in files:
    filepath = os.path.join(base_path, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r') as f:
        content = f.read()
        
    # Pattern to find artifact-left and the subsequent View button's location
    # We use a non-greedy search for the button inside the same artifact-container (roughly)
    # Actually, we can split by artifact-container to be safe.
    
    sections = re.split(r'(<div class="artifact-container[^>]*>)', content)
    new_content = ""
    
    for section in sections:
        if '<div class="artifact-left">' in section:
            # Find the first window.location in this section
            match = re.search(r"onclick=\"window\.location='([^']+)'\"", section)
            if match:
                url = match.group(1)
                section = section.replace('<div class="artifact-left">', f'<div class="artifact-left" onclick="window.location=\'{url}\'">')
        new_content += section
        
    with open(filepath, 'w') as f:
        f.write(new_content)
        
print("Successfully updated artifact-left links in all chapter files.")
