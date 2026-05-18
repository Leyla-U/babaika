#!/usr/bin/env python3
"""
Patch the 8 remaining chapter/index pages that use a different button format.
"""

import os

TARGET_FILES = [
    '/Users/leylaudimamedova/babaika/cheshuya.html',
    '/Users/leylaudimamedova/babaika/il.html',
    '/Users/leylaudimamedova/babaika/index.html',
    '/Users/leylaudimamedova/babaika/kamish.html',
    '/Users/leylaudimamedova/babaika/poloi.html',
    '/Users/leylaudimamedova/babaika/raskaty.html',
    '/Users/leylaudimamedova/babaika/tamarisk.html',
    '/Users/leylaudimamedova/babaika/tuman.html',
]

CART_NOTE_CSS = """    .cart-notes-group {
      padding: 16px 0 8px;
      border-top: 1px solid var(--line);
    }
    .cart-notes-group label {
      display: block;
      font-size: 9px;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--text-faint);
      margin-bottom: 8px;
    }
    .cart-notes-group textarea {
      width: 100%;
      background: transparent;
      border: none;
      border-bottom: 1px solid var(--line);
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 100;
      color: var(--text);
      padding: 6px 0;
      outline: none;
      resize: none;
      min-height: 72px;
      line-height: 1.7;
      transition: border-color 0.2s;
    }
    .cart-notes-group textarea:focus { border-color: var(--text); }
    .cart-notes-group textarea::placeholder { color: var(--text-faint); font-style: italic; font-size: 10px; }
    .cart-notes-hint {
      font-size: 9px;
      color: var(--text-faint);
      font-style: italic;
      line-height: 1.6;
      margin-top: 6px;
    }"""

NOTES_HTML = """<div class="cart-notes-group">
<label for="cart-order-notes">[ Special Notes ]</label>
<textarea id="cart-order-notes" name="order_notes" placeholder="Length, height, or any special requests…" rows="3"></textarea>
<p class="cart-notes-hint">Please leave any special notes or requests here. Babaika is always open to adjusting the length of our wraps to suit your height perfectly. If you have any questions, please contact us before purchasing, or simply specify your preferred length and height in the box above.</p>
</div>
"""

# This is the variant found in chapter pages
CHECKOUT_BTN_ANCHOR = '<button id="checkout-btn" class="btn-glass" disabled>Checkout</button>'

OLD_FETCH_BODY = "body: JSON.stringify({ items }),"
NEW_FETCH_BODY = """body: JSON.stringify({ items, notes: (document.getElementById('cart-order-notes') || {}).value || '' }),"""

OLD_MODAL_TEXTAREA = 'placeholder="Sizes (XS/S/M/L/XL), any special requests, or questions…"'
NEW_MODAL_TEXTAREA = 'placeholder="Please leave any special notes or requests here. Specify preferred wrap length, height, or any other details…"'

OLD_MODAL_LABEL = '<label for="field-sizes">Size / Notes</label>'
NEW_MODAL_LABEL = '<label for="field-sizes">Special Notes / Size</label>'

CSS_CLOSE = '  </style>'

updated = []
errors = []

for filepath in TARGET_FILES:
    filename = os.path.basename(filepath)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'cart-order-notes' in content:
        print(f"⏭  {filename} — already patched")
        continue

    if 'id="cart-sidebar"' not in content and "id='cart-sidebar'" not in content:
        print(f"⏭  {filename} — no cart sidebar")
        continue

    original = content

    # Find the actual button line for debugging
    import re
    matches = re.findall(r'<button[^>]*checkout-btn[^>]*>.*?</button>', content)
    print(f"  {filename} btn variants: {matches}")

    # 1. CSS
    if CSS_CLOSE in content and CART_NOTE_CSS not in content:
        content = content.replace(CSS_CLOSE, CART_NOTE_CSS + '\n' + CSS_CLOSE, 1)

    # 2. Notes HTML — try all known button variants
    anchors = [
        '<button id="checkout-btn" class="btn-glass" disabled>Checkout</button>',
        '<button id="checkout-btn" class="btn-glass" disabled="">Checkout</button>',
        '<button class="btn-glass" disabled="" id="checkout-btn" style="width: 100%;">Checkout</button>',
        '<button class="btn-glass" disabled id="checkout-btn" style="width: 100%;">Checkout</button>',
    ]
    replaced = False
    for anchor in anchors:
        if anchor in content:
            content = content.replace(anchor, NOTES_HTML + anchor, 1)
            replaced = True
            break

    if not replaced:
        errors.append(filename)
        print(f"❌  {filename} — button anchor not found (tried all variants)")
        continue

    # 3. JS fetch
    if OLD_FETCH_BODY in content:
        content = content.replace(OLD_FETCH_BODY, NEW_FETCH_BODY, 1)

    # 4. Formspree modal
    if OLD_MODAL_TEXTAREA in content:
        content = content.replace(OLD_MODAL_TEXTAREA, NEW_MODAL_TEXTAREA, 1)
    if OLD_MODAL_LABEL in content:
        content = content.replace(OLD_MODAL_LABEL, NEW_MODAL_LABEL, 1)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        updated.append(filename)
        print(f"✅  {filename}")
    else:
        print(f"⚠️  {filename} — no changes made")

print(f"\nDone. Updated: {len(updated)}, Errors: {len(errors)}")
