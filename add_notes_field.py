#!/usr/bin/env python3
"""
Adds a "Special Notes" textarea to the cart sidebar across all product pages,
and updates the Stripe fetch call to include the notes value.
"""

import os
import glob

PRODUCT_FILES = glob.glob('/Users/leylaudimamedova/babaika/*.html')
# Exclude non-product pages
EXCLUDE = {'about.html', 'about_es.html', 'about_ru.html', 'index_es.html', 
           'index_ru.html', 'success.html', 'shipping.html', 'catalogue.html',
           'test-product.html'}

# ── CSS to inject (notes textarea in cart) ──────────────────────────────────
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

# ── HTML to inject before the checkout button ────────────────────────────────
NOTES_HTML = """<div class="cart-notes-group">
<label for="cart-order-notes">[ Special Notes ]</label>
<textarea id="cart-order-notes" name="order_notes" placeholder="Length, height, or any special requests…" rows="3"></textarea>
<p class="cart-notes-hint">Please leave any special notes or requests here. Babaika is always open to adjusting the length of our wraps to suit your height perfectly. If you have any questions, please contact us before purchasing, or simply specify your preferred length and height in the box above.</p>
</div>
"""

# Target anchor: the checkout button line in the cart sidebar
CHECKOUT_BTN_ANCHOR = '<button class="btn-glass" disabled="" id="checkout-btn" style="width: 100%;">Checkout</button>'
CHECKOUT_BTN_ANCHOR_ALT = "<button class=\"btn-glass\" disabled id=\"checkout-btn\" style=\"width: 100%;\">Checkout</button>"

# ── JS patch: read notes and send to API ────────────────────────────────────
OLD_FETCH_BODY = "body: JSON.stringify({ items }),"
NEW_FETCH_BODY = """body: JSON.stringify({ items, notes: (document.getElementById('cart-order-notes') || {}).value || '' }),"""

# ── Formspree modal: update placeholder ─────────────────────────────────────
OLD_MODAL_TEXTAREA = 'placeholder="Sizes (XS/S/M/L/XL), any special requests, or questions…"'
NEW_MODAL_TEXTAREA = 'placeholder="Please leave any special notes or requests here. Specify preferred wrap length, height, or any other details…"'

OLD_MODAL_LABEL = '<label for="field-sizes">Size / Notes</label>'
NEW_MODAL_LABEL = '<label for="field-sizes">Special Notes / Size</label>'

# ── CSS anchor: inject before closing </style> ───────────────────────────────
CSS_CLOSE = '  </style>'
CSS_CLOSE_ALT = '</style>'

updated = []
skipped = []
errors = []

for filepath in sorted(PRODUCT_FILES):
    filename = os.path.basename(filepath)
    if filename in EXCLUDE:
        skipped.append(filename)
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if this file doesn't have a cart sidebar
    if 'id="cart-sidebar"' not in content and "id='cart-sidebar'" not in content:
        skipped.append(filename + ' (no cart)')
        continue

    # Skip if notes already added
    if 'cart-order-notes' in content:
        skipped.append(filename + ' (already patched)')
        continue

    original = content

    # 1. Inject CSS before </style>
    if CSS_CLOSE in content:
        content = content.replace(CSS_CLOSE, CART_NOTE_CSS + '\n' + CSS_CLOSE, 1)
    
    # 2. Inject notes HTML before the checkout button
    if CHECKOUT_BTN_ANCHOR in content:
        content = content.replace(CHECKOUT_BTN_ANCHOR, NOTES_HTML + CHECKOUT_BTN_ANCHOR, 1)
    elif CHECKOUT_BTN_ANCHOR_ALT in content:
        content = content.replace(CHECKOUT_BTN_ANCHOR_ALT, NOTES_HTML + CHECKOUT_BTN_ANCHOR_ALT, 1)
    else:
        errors.append(filename + ' — checkout button anchor not found')
        continue

    # 3. Patch JS fetch call to include notes
    if OLD_FETCH_BODY in content:
        content = content.replace(OLD_FETCH_BODY, NEW_FETCH_BODY, 1)

    # 4. Update formspree modal textarea placeholder
    if OLD_MODAL_TEXTAREA in content:
        content = content.replace(OLD_MODAL_TEXTAREA, NEW_MODAL_TEXTAREA, 1)
    if OLD_MODAL_LABEL in content:
        content = content.replace(OLD_MODAL_LABEL, NEW_MODAL_LABEL, 1)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        updated.append(filename)
    else:
        skipped.append(filename + ' (no changes)')

print(f"\n✅ Updated ({len(updated)}):")
for f in updated: print(f"   {f}")
print(f"\n⏭  Skipped ({len(skipped)}):")
for f in skipped: print(f"   {f}")
if errors:
    print(f"\n❌ Errors ({len(errors)}):")
    for f in errors: print(f"   {f}")
