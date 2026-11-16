#!/usr/bin/env python3
"""
Mark the Polói Poplin Kimono (03.02) as sold out everywhere on the site.
"""

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

# ──────────────────────────────────────────────────────────────────────────────
# 1. poloi-wrap-cotton.html — product page: replace "+ Add to Cart" with SOLD OUT
# ──────────────────────────────────────────────────────────────────────────────
def fix_product_page():
    path = os.path.join(BASE, "poloi-wrap-cotton.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    old = '<button class="btn-add-cart btn-glass" data-desc="50% Silk, 50% Cotton Poplin" data-id="03.02" data-name="Polói — Wrap" data-price-id="price_1TQbMZJPn6LmQgwJsozGfeXn" style="flex:1;">+ Add to Cart</button>'
    new = '<button class="btn-glass" disabled style="flex:1; opacity:0.45; cursor:default; pointer-events:none; letter-spacing:0.15em;">SOLD OUT</button>'

    if old not in html:
        print(f"  [WARN] poloi-wrap-cotton.html — add-to-cart button not found (already changed?)")
        return
    html = html.replace(old, new)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  [OK] poloi-wrap-cotton.html — product page button replaced")


# ──────────────────────────────────────────────────────────────────────────────
# 2. catalogue.html — add "Sold Out" badge to cat-item
# ──────────────────────────────────────────────────────────────────────────────
def fix_catalogue():
    path = os.path.join(BASE, "catalogue.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    old = '''        <a href="poloi-wrap-cotton.html" class="cat-item">
          <div class="cat-item-thumb"><img src="https://res.cloudinary.com/dejpm4v8y/image/upload/q_auto,f_auto/v1777153181/psc7_kmsqof.png" alt="Polói Cotton Silk Wrap" loading="lazy" /></div>
          <span class="cat-item-name">Wrap</span>
          <span class="cat-item-desc">50% Silk, 50% Cotton Poplin</span>
          <span class="cat-item-price">$6,000.00 MXN</span>
        </a>'''
    new = '''        <a href="poloi-wrap-cotton.html" class="cat-item" style="opacity:0.6; pointer-events:none;">
          <div class="cat-item-thumb"><img src="https://res.cloudinary.com/dejpm4v8y/image/upload/q_auto,f_auto/v1777153181/psc7_kmsqof.png" alt="Polói Cotton Silk Wrap" loading="lazy" /></div>
          <span class="cat-item-name">Wrap</span>
          <span class="cat-item-desc">50% Silk, 50% Cotton Poplin</span>
          <span class="cat-item-price" style="text-decoration:line-through;">$6,000.00 MXN</span>
          <span class="cat-item-desc" style="letter-spacing:0.15em; font-style:normal;">SOLD OUT</span>
        </a>'''

    if old not in html:
        print(f"  [WARN] catalogue.html — cat-item not found (already changed?)")
        return
    html = html.replace(old, new)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  [OK] catalogue.html — cat-item marked sold out")


# ──────────────────────────────────────────────────────────────────────────────
# 3. All sidebar cat-item listings across product pages
#    Pattern: <a href="poloi-wrap-cotton.html" class="cat-item">
#    Insert sold-out styling and badge, disable link
# ──────────────────────────────────────────────────────────────────────────────
SIDEBAR_FILES = [
    "tamarisk-wrap.html",
    "kamish-wrap-green.html",
    "il-wrap.html",
    "tuman-wrap.html",
    "tamarisk-ring.html",
    "tuman-ring.html",
    "il-ring.html",
    "cheshuya-bra.html",
    "raskaty-wrap.html",
    "tamarisk-scarf.html",
    "raskaty-ring.html",
    "tamarisk-bra.html",
    "tuman-bra.html",
    "cheshuya-necklace.html",
    "raskaty-stockings.html",
    "poloi-bra.html",
    "tuman-earring.html",
    "cheshuya-belt.html",
    "cheshuya-necklace-2.html",
    "kamish-wrap-beige.html",
    "poloi-wrap-cotton.html",  # its own self-reference in sidebar
    "kamish-bag.html",
    "raskaty-ring.html",
    "poloi-wrap.html",  # has poloi-wrap-cotton link in sidebar
]

def fix_sidebar(filename):
    path = os.path.join(BASE, filename)
    if not os.path.exists(path):
        print(f"  [SKIP] {filename} — file not found")
        return

    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Match the cat-item anchor for poloi-wrap-cotton that is NOT already sold-out
    # We look for the pattern and add sold-out label + dim the link
    old_pattern = re.compile(
        r'(<a href="poloi-wrap-cotton\.html" class="cat-item">)'
        r'(\s*<div class="cat-item-thumb">.*?</div>\s*)'
        r'(\s*<span class="cat-item-name">[^<]*</span>)'
        r'(\s*</a>)',
        re.DOTALL
    )

    def replacement(m):
        return (
            '<a href="poloi-wrap-cotton.html" class="cat-item" style="opacity:0.6; pointer-events:none;">'
            + m.group(2)
            + m.group(3)
            + '\n        <span class="cat-item-desc" style="letter-spacing:0.15em; font-style:normal;">SOLD OUT</span>'
            + m.group(4)
        )

    new_html, count = old_pattern.subn(replacement, html)
    if count == 0:
        # Try a simpler match for files that might have different structure
        simple_old = '<a href="poloi-wrap-cotton.html" class="cat-item">'
        simple_new = '<a href="poloi-wrap-cotton.html" class="cat-item" style="opacity:0.6; pointer-events:none;">'
        if simple_old in new_html and simple_new not in new_html:
            new_html = new_html.replace(simple_old, simple_new)
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_html)
            print(f"  [OK] {filename} — link dimmed (simple pattern)")
        else:
            print(f"  [SKIP] {filename} — no matching pattern found (may already be updated)")
        return

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"  [OK] {filename} — {count} cat-item(s) marked sold out")


# ──────────────────────────────────────────────────────────────────────────────
# 4. poloi.html — mark artifact entry as sold out
# ──────────────────────────────────────────────────────────────────────────────
def fix_poloi_page():
    path = os.path.join(BASE, "poloi.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # In poloi.html, the view button links to poloi-wrap-cotton.html
    # Mark the artifact container as sold-out by adding a note and disabling the btn
    old = '          <button onclick="window.location=\'poloi-wrap-cotton.html\'" class="btn-glass" style="width:100%;" data-i18n="btn_view">View</button>'
    new = '          <span style="display:block; font-family:var(--font-mono); font-size:10px; letter-spacing:0.15em; opacity:0.5; margin-bottom:8px;">SOLD OUT</span>\n          <button onclick="window.location=\'poloi-wrap-cotton.html\'" class="btn-glass" style="width:100%; opacity:0.45; pointer-events:none;" disabled>View</button>'

    if old not in html:
        print(f"  [WARN] poloi.html — view button not found (already changed?)")
        return
    html = html.replace(old, new)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  [OK] poloi.html — artifact entry marked sold out")


# ──────────────────────────────────────────────────────────────────────────────
# 5. index.html — mark artifact item as sold out
# ──────────────────────────────────────────────────────────────────────────────
def fix_index():
    path = os.path.join(BASE, "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # In index.html, the poloi-wrap-cotton item is in an artifact-item div
    old = "          <div class=\"artifact-item\" onclick=\"window.location='poloi-wrap-cotton.html'\">"
    new = "          <div class=\"artifact-item\" onclick=\"window.location='poloi-wrap-cotton.html'\" style=\"opacity:0.5; pointer-events:none;\">"

    if old not in html:
        print(f"  [WARN] index.html — artifact-item not found (already changed?)")
        return
    html = html.replace(old, new)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  [OK] index.html — artifact-item dimmed")


# ──────────────────────────────────────────────────────────────────────────────
# Run all fixes
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Marking Polói Poplin Kimono (03.02) as SOLD OUT everywhere...\n")

    fix_product_page()
    fix_catalogue()

    print("\nSidebar cat-items:")
    for f in sorted(set(SIDEBAR_FILES)):
        fix_sidebar(f)

    fix_poloi_page()
    fix_index()

    print("\nDone.")
