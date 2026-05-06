import glob
import re
import json

price_display_map = {}
price_num_map = {}

# 1. Collect all prices
for filepath in glob.glob("*.html"):
    with open(filepath, 'r') as f:
        html = f.read()
    
    price_match = re.search(r'Price:\s*(\$[^<]+)', html)
    if not price_match:
        continue
    price_str = price_match.group(1).strip() # e.g. $6,000.00 MXN
    
    num_str = price_str.replace('$', '').replace(' MXN', '').replace(',', '')
    try:
        price_num = float(num_str)
    except:
        price_num = 0
    
    matches = re.finditer(r'<button[^>]*class=["\'][^"\']*\bbtn-add-cart\b[^>]*>', html)
    for m in matches:
        btn = m.group(0)
        id_match = re.search(r'data-id="([^"]+)"', btn)
        if id_match:
            price_display_map[id_match.group(1)] = price_str
            price_num_map[id_match.group(1)] = price_num

print(f"Found {len(price_num_map)} prices.")

js_injection = f"""
    const PRICE_NUM_MAP = {json.dumps(price_num_map)};
    const PRICE_DISP_MAP = {json.dumps(price_display_map)};
"""

# 2. Inject map and modify cart rendering in all files
for filepath in glob.glob("*.html"):
    with open(filepath, 'r') as f:
        html = f.read()
        
    if "const PRICE_NUM_MAP" not in html:
        # Inject the maps after PRICE_ID_MAP
        html = re.sub(r'(const PRICE_ID_MAP = [^;]+;)', r'\1' + js_injection, html)
    
    # 3. Replace "Price on inquiry" with dynamic price
    # Look for: <span class="cart-item-price">Price on inquiry</span>
    html = re.sub(
        r'<span class="cart-item-price">Price on inquiry</span>',
        r'<span class="cart-item-price">${(typeof PRICE_DISP_MAP !== "undefined" && PRICE_DISP_MAP[item.id]) ? PRICE_DISP_MAP[item.id] : "Price on inquiry"}</span>',
        html
    )
    
    # 4. Replace cartTotal logic
    # Look for: cartTotal.textContent = `${totalItems} piece${totalItems > 1 ? 's' : ''} — price on inquiry`;
    # or the whole block:
    # const totalItems = cart.reduce((s, i) => s + i.qty, 0);
    # cartTotal.textContent = ...
    
    total_logic_old = r"const totalItems = cart\.reduce\(\(s, i\) => s \+ i\.qty, 0\);\s*cartTotal\.textContent = `\$\{totalItems\} piece\$\{\w+ > 1 \? 's' : ''\} — price on inquiry`;"
    
    total_logic_new = """const totalItems = cart.reduce((s, i) => s + i.qty, 0);
      let totalPrice = 0;
      let allPriced = true;
      cart.forEach(i => {
        if (typeof PRICE_NUM_MAP !== "undefined" && PRICE_NUM_MAP[i.id]) {
            totalPrice += PRICE_NUM_MAP[i.id] * i.qty;
        } else {
            allPriced = false;
        }
      });
      if (allPriced && totalPrice > 0) {
        cartTotal.textContent = `${totalItems} piece${totalItems > 1 ? 's' : ''} — $${totalPrice.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})} MXN`;
      } else {
        cartTotal.textContent = `${totalItems} piece${totalItems > 1 ? 's' : ''} — price on inquiry`;
      }"""
      
    html = re.sub(total_logic_old, total_logic_new, html)
    
    # Also update the empty cart total text
    # cartTotal.textContent = 'Price on inquiry'; -> when empty, it can just be empty or "—"
    # Actually, keep it 'Price on inquiry' when empty, or change it to "$0.00 MXN" if requested. The user just asked to place the prices, so keeping the empty state as is is fine.
    
    with open(filepath, 'w') as f:
        f.write(html)
    print(f"Updated {filepath}")
