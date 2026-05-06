import re

with open("tuman.html", "r") as f:
    content = f.read()

original = content

# Replace Earring price
def fix_earring(match):
    block = match.group(0)
    return re.sub(r'Price:\s*\$[0-9,]+\.00\s*MXN', 'Price: $1,400.00 MXN', block)

content = re.sub(r'<div class="artifact-left" onclick="window\.location=\'tuman-earring\.html\'">[\s\S]*?</div>\s*</div>', fix_earring, content)

# Replace Ring price
def fix_ring(match):
    block = match.group(0)
    return re.sub(r'Price:\s*\$[0-9,]+\.00\s*MXN', 'Price: $2,900.00 MXN', block)

content = re.sub(r'<div class="artifact-left" onclick="window\.location=\'tuman-ring\.html\'">[\s\S]*?</div>\s*</div>', fix_ring, content)

if content != original:
    with open("tuman.html", "w") as f:
        f.write(content)
    print("Fixed tuman.html prices!")
else:
    print("No changes made.")

