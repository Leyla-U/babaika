#!/usr/bin/env python3
"""
Archive the Poloi ring from the entire site.
- poloi.html: remove the full artifact section (lines ~1251-1277)
- index.html: remove the RING artifact-item in chapter 03
- catalogue.html: replace poloi-ring cat-item with invisible spacer
- poloi-bra.html: remove the "match with" ring card
- poloi-wrap-cotton.html: remove the "match with" ring card
- All catalogue overlays (cat-item in Ch03): replace with invisible spacer
"""

import re
import os

BASE = "/Users/leylaudimamedova/babaika"

# ─── 1. poloi.html — remove entire ring artifact section ─────────────────────
path = os.path.join(BASE, "poloi.html")
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove the artifact section block
old = """
  <!-- ARTIFACT 05: RING -->
  <div class="artifact-container reveal">
    <div class="artifact-header">
      <p class="artifact-tag">[ HARDWARE ARTIFACT 03.04 ]</p>
    </div>
    <div class="artifact-grid">
      <div class="artifact-left" onclick="window.location='poloi-ring.html'">
        <p class="artifact-name">THE FLOODED SURFACE</p>
        <p class="artifact-detail-row">Material: Silver</p>
        <p class="artifact-detail-row" style="margin-top:8px;">Price: $2,400.00 MXN</p>
        <div class="artifact-actions" style="margin-top: 24px; display: flex; flex-direction: column; gap: 8px;">
          <button onclick="window.location='poloi-ring.html'" class="btn-glass" style="width:100%;" data-i18n="btn_view">View</button>
        </div>
      </div>
      <div class="artifact-center" onclick="window.location='poloi-ring.html'">
        <div class="photo-viewer">
          <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/q_auto,f_auto/v1777257313/poloi_ring_bw_ut3b82.png" class="main-photo" alt="Ring" style="cursor: none;" />
        </div>
      </div>
      <div class="artifact-right">
        <p class="artifact-note">
          <strong style="font-style:normal; font-weight:200; letter-spacing:0.08em;" data-i18n="lbl_translation">[ TRANSLATION NOTE ]</strong><br><br>
          Translates the subtle kinetic energy of the shallow water claiming the land. The silver is sculpted to capture a continuous field of small, undulating waves - freezing the exact physical tension of the fluid layer as it evenly covers and consumes the terrestrial surface beneath it.
        </p>
      </div>
    </div>
  </div>"""

if old in content:
    content = content.replace(old, "")
    print("✓ poloi.html: removed ring artifact section")
else:
    print("✗ poloi.html: ring artifact section NOT found — check manually")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)


# ─── 2. index.html — remove RING artifact-item in chapter 03 ─────────────────
path = os.path.join(BASE, "index.html")
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """          
          <p class="artifact-section-title" data-i18n="lbl_hardware">[ HARDWARE ARTIFACTS ]</p>
          
          <div class="artifact-item" onclick="window.location='poloi-ring.html'">
            <p class="artifact-title">RING</p>
            <p class="artifact-desc">Silver</p>
          </div>"""

new = ""

if old in content:
    content = content.replace(old, "")
    print("✓ index.html: removed ring artifact-item")
else:
    print("✗ index.html: ring artifact-item NOT found — check manually")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)


# ─── 3. catalogue.html — replace poloi-ring with invisible spacer ─────────────
path = os.path.join(BASE, "catalogue.html")
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """        <a href="poloi-ring.html" class="cat-item">
          <div class="cat-item-thumb"><video preload="none" src="https://res.cloudinary.com/dejpm4v8y/video/upload/q_auto,f_auto,vc_auto/v1777085497/raskaty-ring_rqvurs.mp4" autoplay loop muted playsinline></video></div>
          <span class="cat-item-name">Ring</span>
          <span class="cat-item-desc">Silver</span>
          <span class="cat-item-price">$2,400.00 MXN</span>
        </a>"""
new = """        <div class="cat-item" style="opacity:0; pointer-events:none;"></div>"""

if old in content:
    content = content.replace(old, new)
    print("✓ catalogue.html: replaced ring with spacer")
else:
    print("✗ catalogue.html: ring entry NOT found — check manually")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)


# ─── 4. poloi-bra.html — remove ring card from "match with" section ──────────
path = os.path.join(BASE, "poloi-bra.html")
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Find and remove the ring match-with card (3 lines: div + p + p + /div)
pattern = r'<div onclick="window\.location=\'poloi-ring\.html\'" style="cursor: pointer;">\s*<video[^>]*>[^<]*</video>\s*<p[^>]*>.*?</p>\s*<p[^>]*>The Flooded Surface</p>\s*</div>'
new_content = re.sub(pattern, '', content, flags=re.DOTALL)
if new_content != content:
    print("✓ poloi-bra.html: removed ring match-with card")
    content = new_content
else:
    print("✗ poloi-bra.html: ring match-with card NOT found — check manually")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)


# ─── 5. poloi-wrap-cotton.html — remove ring card from "match with" ───────────
path = os.path.join(BASE, "poloi-wrap-cotton.html")
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

pattern = r'<div onclick="window\.location=\'poloi-ring\.html\'" style="cursor: pointer;">\s*<video[^>]*>[^<]*</video>\s*<p[^>]*>.*?</p>\s*<p[^>]*>The Flooded Surface</p>\s*</div>'
new_content = re.sub(pattern, '', content, flags=re.DOTALL)
if new_content != content:
    print("✓ poloi-wrap-cotton.html: removed ring match-with card")
    content = new_content
else:
    print("✗ poloi-wrap-cotton.html: ring match-with card NOT found — check manually")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)


# ─── 6. All catalogue overlays — replace poloi-ring cat-item with spacer ──────
# Pattern used in every product page's embedded catalogue overlay
CAT_OVERLAY_PATTERN = re.compile(
    r'<a href="poloi-ring\.html" class="cat-item">\s*'
    r'<div class="cat-item-thumb"><video[^>]*>[^<]*</video></div>\s*'
    r'<span class="cat-item-name">The Flooded Surface</span>\s*'
    r'</a>',
    re.DOTALL
)
SPACER = '<div class="cat-item" style="opacity:0; pointer-events:none;"></div>'

html_files = [f for f in os.listdir(BASE) if f.endswith(".html")]
for fname in sorted(html_files):
    # Skip files already handled above or not relevant
    if fname in ("poloi.html", "index.html", "catalogue.html", "poloi-bra.html",
                 "poloi-wrap-cotton.html", "poloi-ring.html"):
        continue
    fpath = os.path.join(BASE, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    new_content, count = CAT_OVERLAY_PATTERN.subn(SPACER, content)
    if count:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✓ {fname}: replaced {count} cat-item(s) with spacer")

print("\nDone.")
