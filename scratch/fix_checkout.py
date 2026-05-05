import os
import glob
import re

def fix_checkout_priceid(filepath):
    with open(filepath, 'r') as f:
        html = f.read()
        
    original = html
    
    # Let's see if PRICE_MAP exists in the file, we can inject PRICE_ID_MAP next to it.
    if 'const PRICE_MAP =' in html and 'const PRICE_ID_MAP =' not in html:
        # Build PRICE_ID_MAP for this file/all files
        # Actually, let's just build it by scanning all files again inside Python
        price_id_map = {}
        for f2 in glob.glob("*.html"):
            if f2.startswith("index_") or f2.startswith("about_"):
                continue
            with open(f2, 'r') as file2:
                html2 = file2.read()
                matches = re.finditer(r'<button[^>]*class=["\'][^"\']*\bbtn-add-cart\b[^>]*>', html2)
                for m in matches:
                    btn_tag = m.group(0)
                    id_match = re.search(r'data-id="([^"]+)"', btn_tag)
                    price_id_match = re.search(r'data-price-id="([^"]+)"', btn_tag)
                    if id_match and price_id_match:
                        price_id_map[id_match.group(1)] = price_id_match.group(1)
        
        map_js = "const PRICE_ID_MAP = " + str(price_id_map) + ";"
        
        html = re.sub(r'(const PRICE_MAP = \{.*?\};)', r'\1\n    ' + map_js, html)
        
    # Now update redirectToStripe
    # Original:
    # const items = cart
    #   .filter(i => i.priceId)
    #   .map(i => ({ priceId: i.priceId, quantity: i.qty }));
    
    # New:
    # const items = cart
    #   .map(i => ({ priceId: i.priceId || PRICE_ID_MAP[i.id], quantity: i.qty }))
    #   .filter(i => i.priceId);
    
    html = re.sub(
        r'const items = cart\s*\.filter\(i => i\.priceId\)\s*\.map\(i => \(\{ priceId: i\.priceId, quantity: i\.qty \}\)\);',
        r'const items = cart\n        .map(i => ({ priceId: i.priceId || (typeof PRICE_ID_MAP !== "undefined" ? PRICE_ID_MAP[i.id] : undefined), quantity: i.qty }))\n        .filter(i => i.priceId);',
        html
    )
    
    if html != original:
        with open(filepath, 'w') as f:
            f.write(html)
        print(f"Fixed checkout logic in {filepath}")

for f in glob.glob("*.html"):
    if not f.startswith("index_") and not f.startswith("about_"):
        fix_checkout_priceid(f)
