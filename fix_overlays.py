import re

def fix_overlay(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    new_chapter_03 = """    <div class="cat-chapter">
      <p class="cat-chapter-title">Chapter 03 — Polói</p>
      <div class="cat-row">
        <a href="poloi-kimono.html" class="cat-item">
          <div class="cat-item-thumb"><video src="https://res.cloudinary.com/dejpm4v8y/video/upload/v1777169031/pc2_fsgmnp.mp4" autoplay loop muted playsinline></video></div>
          <span class="cat-item-name">03.01 Polói Kimono</span>
        </a>
        <a href="poloi-bra.html" class="cat-item">
          <div class="cat-item-thumb"><img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152373/babaika_delta_30_rzpquc.jpg" alt=""/></div>
          <span class="cat-item-name">03.03 Soft Bra</span>
        </a>
        <a href="poloi-ring.html" class="cat-item">
          <div class="cat-item-thumb"><video src="https://res.cloudinary.com/dejpm4v8y/video/upload/v1777085497/raskaty-ring_rqvurs.mp4" autoplay loop muted playsinline></video></div>
          <span class="cat-item-name">03.04 The Flooded Surface</span>
        </a>
        <a href="poloi-kimono-cotton.html" class="cat-item">
          <div class="cat-item-thumb"><img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777153181/psc7_kmsqof.png" alt=""/></div>
          <span class="cat-item-name">03.02 Polói Kimono (Cotton)</span>
        </a>
      </div>
    </div>"""

    new_chapter_04 = """    <div class="cat-chapter">
      <p class="cat-chapter-title">Chapter 04 — Il</p>
      <div class="cat-row">
        <a href="il-kimono.html" class="cat-item">
          <div class="cat-item-thumb"><img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777182384/il111111_ft12bx.png" alt=""/></div>
          <span class="cat-item-name">Il Kimono</span>
        </a>
        <a href="il-ring.html" class="cat-item">
          <div class="cat-item-thumb"><video src="https://res.cloudinary.com/dejpm4v8y/video/upload/v1777085494/il-ring_lpipgo.mp4" autoplay loop muted playsinline></video></div>
          <span class="cat-item-name">Il Ring</span>
        </a>
        <div class="cat-item" style="opacity:0; pointer-events:none;"></div>
        <div class="cat-item" style="opacity:0; pointer-events:none;"></div>
      </div>
    </div>"""

    # Replace the old Chapter 03 block (which was wrongly named Il in the copy)
    content = re.sub(
        r'<div class="cat-chapter">\s*<p class="cat-chapter-title">Chapter 03 — Il</p>.*?</div>\s*</div>',
        new_chapter_03 + "\n" + new_chapter_04 + "\n  </div>",
        content,
        flags=re.DOTALL
    )
    
    with open(filename, 'w') as f:
        f.write(content)

fix_overlay('il-kimono.html')
fix_overlay('il-ring.html')
