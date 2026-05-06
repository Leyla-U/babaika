import glob
import re

price_map = {}

# 1. Collect all data-ids and price-ids
for filepath in glob.glob("*.html"):
    with open(filepath, 'r') as f:
        html = f.read()
        
    matches = re.finditer(r'<button[^>]*class=["\'][^"\']*\bbtn-add-cart\b[^>]*>', html)
    for m in matches:
        btn = m.group(0)
        id_match = re.search(r'data-id="([^"]+)"', btn)
        price_match = re.search(r'data-price-id="([^"]+)"', btn)
        if id_match and price_match:
            price_map[id_match.group(1)] = price_match.group(1)

print(f"Found {len(price_map)} price mappings.")

map_js = "\n    const PRICE_ID_MAP = " + str(price_map) + ";\n"

# 2. Inject PRICE_ID_MAP into every file if not present
for filepath in glob.glob("*.html"):
    with open(filepath, 'r') as f:
        html = f.read()
    
    if "const PRICE_ID_MAP =" in html:
        continue # already injected
        
    # Inject it right inside the IIFE of the cart script
    # Look for let cart = JSON.parse(localStorage.getItem('babaika_cart') || '[]');
    
    target = r"(let cart = JSON\.parse\(localStorage\.getItem\('babaika_cart'\) \|\| '\[\]'\);)"
    
    if re.search(target, html):
        html = re.sub(target, r'\1' + map_js, html)
        with open(filepath, 'w') as f:
            f.write(html)
        print(f"Injected map in {filepath}")

