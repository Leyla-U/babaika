import os
import glob
import re

def build_price_map():
    price_map = {}
    # Scan all files to find <button ... data-id="XX.XX" ... data-price="YYYY"
    for f in glob.glob("*.html"):
        if f.startswith("index_") or f.startswith("about_"):
            continue
        with open(f, 'r') as file:
            html = file.read()
            # find all btn-add-cart and extract data-id and data-price
            matches = re.finditer(r'<button[^>]*class=["\'][^"\']*\bbtn-add-cart\b[^>]*>', html)
            for m in matches:
                btn_tag = m.group(0)
                
                id_match = re.search(r'data-id="([^"]+)"', btn_tag)
                price_match = re.search(r'data-price="([^"]+)"', btn_tag)
                
                if id_match and price_match:
                    price_map[id_match.group(1)] = int(price_match.group(1))
    return price_map

PRICE_MAP = build_price_map()
price_map_js = "const PRICE_MAP = " + str(PRICE_MAP) + ";"

def update_file(filepath):
    with open(filepath, 'r') as file:
        html = file.read()
        
    original = html
    
    # 1. Export TRANSLATIONS to window
    # find const TRANSLATIONS = {
    # and we want to inject window.TRANSLATIONS = TRANSLATIONS; after it
    # The safest way is to replace `var lang = localStorage.getItem...` with `window.TRANSLATIONS = TRANSLATIONS; var lang = ...`
    html = re.sub(
        r'(var lang\s*=\s*localStorage\.getItem\(\'babaika_lang\'\)\s*\|\|\s*\'en\';)',
        r'window.TRANSLATIONS = TRANSLATIONS;\n    \1',
        html
    )
    
    # 2. Update renderCart()
    # We will completely replace the renderCart() function with a new one
    
    new_render_cart = f"""
    {price_map_js}
    
    function getTranslation(engText) {{
       const currentLang = localStorage.getItem('babaika_lang') || 'en';
       if (currentLang === 'en' || !window.TRANSLATIONS) return engText;
       const enDict = window.TRANSLATIONS['en'];
       const esDict = window.TRANSLATIONS['es'];
       for (let k in enDict) {{
           if (enDict[k] === engText) return esDict[k] || engText;
       }}
       return engText;
    }}

    function renderCart() {{
      const total = cart.reduce((s, i) => s + i.qty, 0);
      cartCount.textContent = total;
      
      checkoutBtn.disabled = cart.length === 0;

      if (cart.length === 0) {{
        cartItemsEl.innerHTML = '<p class="cart-empty" data-i18n="cart_empty_4">No artifacts selected.<br>Each piece is made to order.</p>';
        const currentLang = localStorage.getItem('babaika_lang') || 'en';
        cartTotal.textContent = (currentLang === 'es') ? 'Precio a consultar' : 'Price on inquiry';
        return;
      }}

      cartItemsEl.innerHTML = '';
      cart.forEach((item, idx) => {{
        const p = item.price || PRICE_MAP[item.id] || 0;
        const div = document.createElement('div');
        div.className = 'cart-item';
        div.innerHTML = `
          <div class="cart-item-header">
            <span class="cart-item-title">${{getTranslation(item.name)}}</span>
            <button class="cart-item-remove" data-idx="${{idx}}" aria-label="Remove">×</button>
          </div>
          <span class="cart-item-meta">${{getTranslation(item.desc)}}</span>
          <div class="cart-qty-row">
            <button class="cart-qty-btn" data-action="dec" data-idx="${{idx}}">−</button>
            <span class="cart-qty-num">${{item.qty}}</span>
            <button class="cart-qty-btn" data-action="inc" data-idx="${{idx}}">+</button>
            <span class="cart-item-price">$${{(p * item.qty).toLocaleString("en-US")}} MXN</span>
          </div>`;
        cartItemsEl.appendChild(div);
      }});

      const totalItems = cart.reduce((s, i) => s + i.qty, 0);
      const totalSum = cart.reduce((s, i) => s + ((i.price || PRICE_MAP[i.id] || 0) * i.qty), 0);
      
      const currentLang = localStorage.getItem('babaika_lang') || 'en';
      const pieceStr = (currentLang === 'es') ? (totalItems !== 1 ? "piezas" : "pieza") : (totalItems !== 1 ? "pieces" : "piece");
      cartTotal.textContent = `${{totalItems}} ${{pieceStr}} — $${{totalSum.toLocaleString("en-US")}} MXN`;

      // qty / remove handlers
      cartItemsEl.querySelectorAll('.cart-item-remove').forEach(btn => {{
        btn.addEventListener('click', () => {{ cart.splice(+btn.dataset.idx, 1); save(); renderCart(); bumpCount(); }});
      }});
      cartItemsEl.querySelectorAll('.cart-qty-btn').forEach(btn => {{
        btn.addEventListener('click', () => {{
          const i = +btn.dataset.idx;
          if (btn.dataset.action === 'inc') {{ cart[i].qty++; }}
          else {{ cart[i].qty--; if (cart[i].qty <= 0) cart.splice(i, 1); }}
          save(); renderCart(); bumpCount();
        }});
      }});
    }}
    """
    
    # We need to replace the old renderCart function
    # The old one starts at function renderCart() { and ends at the closing brace before function bumpCount() {
    # Since we also have some other constants, let's just use regex to replace it
    
    # This regex captures function renderCart() { ... } down to just before function bumpCount()
    html = re.sub(
        r'function renderCart\(\)\s*\{[\s\S]*?(?=function bumpCount\(\)\s*\{)',
        new_render_cart + "\n\n    ",
        html
    )
    
    if html != original:
        with open(filepath, 'w') as f:
            f.write(html)
        print(f"Updated {filepath}")

for f in glob.glob("*.html"):
    if not f.startswith("index_") and not f.startswith("about_"):
        update_file(f)
