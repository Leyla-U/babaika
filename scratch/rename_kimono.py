import glob
import os
import re
import subprocess

# Find all html files
all_html = glob.glob("*.html")

# Find the ones to rename
to_rename = [f for f in all_html if "kimono" in f]

renames = {}
for old_name in to_rename:
    new_name = old_name.replace("kimono", "wrap")
    renames[old_name] = new_name

print("Renames to process:", renames)

# Step 1: Update the links in all HTML files BEFORE renaming them
# We do this in-memory for all files
for filepath in all_html:
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    # Replace all occurrences of old_name with new_name in the text
    for old_name, new_name in renames.items():
        content = content.replace(old_name, new_name)
    
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated links in {filepath}")

# Step 2: Use git mv to rename the files
for old_name, new_name in renames.items():
    subprocess.run(["git", "mv", old_name, new_name], check=True)
    print(f"Renamed {old_name} -> {new_name}")

