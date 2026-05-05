import os
import glob
import re

def update_prices_in_html(filepath):
    with open(filepath, 'r') as f:
        html = f.read()
        
    original = html
    
    # 1. Update the cart rendering logic in the JS
    # We replace:
    # <span class="cart-item-price" data-i18n="final_auto_span_38">Price on inquiry</span>
    # with:
    # <span class="cart-item-price">$${(item.price * item.qty).toLocaleString('en-US')} MXN</span>
    
    html = re.sub(
        r'<span class="cart-item-price"[^>]*>.*?Price on inquiry.*?</span>',
        r'<span class="cart-item-price">$$${(item.price * item.qty).toLocaleString("en-US")} MXN</span>',
        html,
        flags=re.IGNORECASE
    )
    
    # Update the cartTotal textContent logic
    # cartTotal.textContent = `${totalItems} piece${totalItems > 1 ? 's' : ''} — price on inquiry`;
    # or similar
    
    html = re.sub(
        r'cartTotal\.textContent\s*=\s*`\$\{totalItems\} piece\$\{.*?\}\s*—\s*price on inquiry`;?',
        r'const totalSum = cart.reduce((s, i) => s + (i.price * i.qty), 0);\n      cartTotal.textContent = `${totalItems} piece${totalItems !== 1 ? "s" : ""} — $${totalSum.toLocaleString("en-US")} MXN`;',
        html,
        flags=re.IGNORECASE
    )
    
    # Update addToCart to extract price
    # const { id, priceId, name, desc } = btn.dataset;
    # cart.push({ id, priceId, name, desc, qty: 1 });
    
    html = re.sub(
        r'const { id, priceId, name, desc } = btn\.dataset;',
        r'const { id, priceId, name, desc, price } = btn.dataset;\n        const numPrice = parseInt((price || "0").replace(/,/g, ""), 10);',
        html
    )
    
    html = re.sub(
        r'cart\.push\(\{\s*id,\s*priceId,\s*name,\s*desc,\s*qty:\s*1\s*\}\);',
        r'cart.push({ id, priceId, name, desc, price: numPrice, qty: 1 });',
        html
    )
    
    # 2. Inject data-price="1600" into btn-add-cart
    # This requires looking for the Price: $X,XXX.00 MXN string that comes right before the button
    
    # A safe way is to split the document by btn-add-cart and look backwards for the price
    # Wait, regex might be easier.
    # Pattern: <p ...>Price: $1,600.00 MXN</p> ... <button class="btn-add-cart..."
    
    # We can find all prices first, but some pages have multiple
    # Let's use a regex to match the block:
    # Price:\s*\$([0-9,]+)\.00\s*MXN[\s\S]*?(<button[^>]*class=["'][^"']*btn-add-cart[^>]*>)
    
    def replacer_price(m):
        price_str = m.group(1).replace(',', '')
        btn_tag = m.group(2)
        
        if 'data-price=' not in btn_tag:
            # insert data-price before class or after button
            new_btn = btn_tag.replace('class=', f'data-price="{price_str}" class=')
            return m.group(0).replace(btn_tag, new_btn)
        return m.group(0)
        
    html = re.sub(r'Price:\s*\$([0-9,]+)\.00\s*MXN([\s\S]{1,500}?)(<button[^>]*class=["\'][^"\']*\bbtn-add-cart\b[^>]*>)', replacer_price, html, flags=re.IGNORECASE)
    
    if html != original:
        with open(filepath, 'w') as f:
            f.write(html)
        print(f"Updated prices in {filepath}")

for f in glob.glob("*.html"):
    if not f.startswith("index_") and not f.startswith("about_"):
        update_prices_in_html(f)
