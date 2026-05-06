import glob
import re

price_display_map = {}

# We need to map data-id -> Display Price (e.g. "$6,000.00 MXN")
for filepath in glob.glob("*.html"):
    with open(filepath, 'r') as f:
        html = f.read()
    
    # Extract the price if present
    price_match = re.search(r'Price:\s*(\$[^<]+)', html)
    if not price_match:
        continue
    price_str = price_match.group(1).strip()
    
    # Find the data-id for this page's button
    matches = re.finditer(r'<button[^>]*class=["\'][^"\']*\bbtn-add-cart\b[^>]*>', html)
    for m in matches:
        btn = m.group(0)
        id_match = re.search(r'data-id="([^"]+)"', btn)
        if id_match:
            price_display_map[id_match.group(1)] = price_str

print(f"Found {len(price_display_map)} price display mappings.")
print(price_display_map)
