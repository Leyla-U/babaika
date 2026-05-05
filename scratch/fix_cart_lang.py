import os
import glob
import re

def fix_cart_and_lang(filepath):
    with open(filepath, 'r') as f:
        html = f.read()
        
    original = html
    
    # 1. Update the cartTotal.textContent to support language toggle
    html = re.sub(
        r'cartTotal\.textContent\s*=\s*`\$\{totalItems\} piece\$\{totalItems !== 1 \? "s" : ""\} — \$\$\{totalSum\.toLocaleString\("en-US"\)\} MXN`;',
        r'const pieceStr = (typeof lang !== "undefined" && lang === "es") ? (totalItems !== 1 ? "piezas" : "pieza") : (totalItems !== 1 ? "pieces" : "piece");\n      cartTotal.textContent = `${totalItems} ${pieceStr} — $${totalSum.toLocaleString("en-US")} MXN`;',
        html
    )
    
    # 2. Add renderCart() to applyLang
    # find applyLang(l) { ... }
    # Before the end of the function, inject renderCart
    if 'if (typeof renderCart === \'function\') renderCart();' not in html:
        html = re.sub(
            r'(\[\'footer-lang-\',\s*\'lang-\'\].forEach\(function\(prefix\)\s*\{[\s\S]*?\}\);\s*\}\);\s*)(\})',
            r'\1  if (typeof renderCart === "function") renderCart();\n    \2',
            html
        )
        
    # 3. Make sure id="cart-total" has no data-i18n that would overwrite it
    html = re.sub(r'id="cart-total"\s*data-i18n="[^"]*"', 'id="cart-total"', html)
    
    if html != original:
        with open(filepath, 'w') as f:
            f.write(html)
        print(f"Fixed cart rendering in {filepath}")

for f in glob.glob("*.html"):
    if not f.startswith("index_") and not f.startswith("about_"):
        fix_cart_and_lang(f)
