import os
import re

master_overlay_inner = """
    <div class="cat-header">
      <span class="cat-title">Babaika</span>
      <button onclick="closeCatalogue()" style="background:none; border:none; font-family:var(--font-mono); font-size:11px; letter-spacing:0.2em; color:var(--text-faint); cursor:none; text-transform:uppercase;">[ CLOSE ]</button>
    </div>
    <div class="cat-chapter">
      <p class="cat-chapter-title">Chapter 01 — Tuman</p>
      <div class="cat-row">
        <a href="tuman-kimono.html" class="cat-item">
          <div class="cat-item-thumb"><img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777229442/babaika_film_18_aglteu.jpg" alt=""/></div>
          <span class="cat-item-name">Tuman Kimono</span>
        </a>
        <a href="tuman-bra.html" class="cat-item">
          <div class="cat-item-thumb"><img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777232154/babaika_film_12_kisi4o.jpg" alt=""/></div>
          <span class="cat-item-name">Tuman Soft Bra</span>
        </a>
        <a href="tuman-earring.html" class="cat-item">
          <div class="cat-item-thumb"><img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777231902/te1_kjzxym.png" alt=""/></div>
          <span class="cat-item-name">Tuman Earring</span>
        </a>
        <a href="tuman-ring.html" class="cat-item">
          <div class="cat-item-thumb"><video src="https://res.cloudinary.com/dejpm4v8y/video/upload/v1777085507/tuman-ring_cgwnu3.mp4" autoplay loop muted playsinline></video></div>
          <span class="cat-item-name">Tuman Ring</span>
        </a>
      </div>
    </div>
    <div class="cat-chapter">
      <p class="cat-chapter-title">Chapter 02 — Tamarisk</p>
      <div class="cat-row">
        <a href="tamarisk-kimono.html" class="cat-item">
          <div class="cat-item-thumb"><img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777182363/tmr111_smm4lt.png" alt=""/></div>
          <span class="cat-item-name">Tamarisk Kimono</span>
        </a>
        <a href="tamarisk-bra.html" class="cat-item">
          <div class="cat-item-thumb"><img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777167754/tmr123_mjl8ib.png" alt=""/></div>
          <span class="cat-item-name">Tamarisk Bra</span>
        </a>
        <a href="tamarisk-ring.html" class="cat-item">
          <div class="cat-item-thumb"><video src="https://res.cloudinary.com/dejpm4v8y/video/upload/v1777082418/tamarisk_ring_vxj0td.mp4" autoplay loop muted playsinline></video></div>
          <span class="cat-item-name">Tamarisk Ring</span>
        </a>
        <a href="tamarisk-scarf.html" class="cat-item">
          <div class="cat-item-thumb"><img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152062/tmsc1_s1v1y5.png" alt=""/></div>
          <span class="cat-item-name">Tamarisk Scarf</span>
        </a>
      </div>
    </div>
    <div class="cat-chapter">
      <p class="cat-chapter-title">Chapter 03 — Polói</p>
      <div class="cat-row">
        <a href="poloi-kimono.html" class="cat-item">
          <div class="cat-item-thumb"><img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173937/babaika_film_03_hnyeed.jpg" alt=""/></div>
          <span class="cat-item-name">Polói Kimono</span>
        </a>
        <a href="poloi-kimono-cotton.html" class="cat-item">
          <div class="cat-item-thumb"><img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777233449/poloidd_bzraoq.png" alt=""/></div>
          <span class="cat-item-name">Polói Kimono (Cotton)</span>
        </a>
        <a href="poloi-bra.html" class="cat-item">
          <div class="cat-item-thumb"><video src="https://res.cloudinary.com/dejpm4v8y/video/upload/v1777172643/poloic_uyjq9u.mp4" autoplay loop muted playsinline></video></div>
          <span class="cat-item-name">Polói Bra</span>
        </a>
        <a href="poloi-ring.html" class="cat-item">
          <div class="cat-item-thumb"><video src="https://res.cloudinary.com/dejpm4v8y/video/upload/v1777085497/raskaty-ring_rqvurs.mp4" autoplay loop muted playsinline></video></div>
          <span class="cat-item-name">The Flooded Surface</span>
        </a>
      </div>
    </div>
    <div class="cat-chapter">
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
    </div>
    <div class="cat-chapter">
      <p class="cat-chapter-title">Chapter 05 — Raskáty</p>
      <div class="cat-row">
        <a href="raskaty-kimono.html" class="cat-item">
          <div class="cat-item-thumb"><img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777255323/raskaty-kimono2_hzu2xz.png" alt=""/></div>
          <span class="cat-item-name">05.01 Kimono</span>
        </a>
        <a href="raskaty-stockings.html" class="cat-item">
          <div class="cat-item-thumb"><img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777182275/SHE00304_prorin.png" alt=""/></div>
          <span class="cat-item-name">05.02 Stockings</span>
        </a>
        <a href="raskaty-ring.html" class="cat-item">
          <div class="cat-item-thumb"><video src="https://res.cloudinary.com/dejpm4v8y/video/upload/v1777085493/raskaty-ring2_qok5zn.mp4" autoplay loop muted playsinline></video></div>
          <span class="cat-item-name">05.03 Ring</span>
        </a>
        <div class="cat-item" style="opacity:0; pointer-events:none;"></div>
      </div>
    </div>
    <div class="cat-chapter">
      <p class="cat-chapter-title">Chapter 06 — Kamish</p>
      <div class="cat-row">
        <a href="kamish-kimono-beige.html" class="cat-item">
          <div class="cat-item-thumb"><img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777182833/SHE00023_etr9np.png" alt=""/></div>
          <span class="cat-item-name">06.01 Kimono (Beige)</span>
        </a>
        <a href="kamish-kimono-green.html" class="cat-item">
          <div class="cat-item-thumb"><video src="https://res.cloudinary.com/dejpm4v8y/video/upload/v1777175218/kamish1_vrnrqx.mp4" autoplay loop muted playsinline></video></div>
          <span class="cat-item-name">06.02 Kimono (Green)</span>
        </a>
        <a href="kamish-bag.html" class="cat-item">
          <div class="cat-item-thumb"><img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777184256/kambag_vyraac.png" alt=""/></div>
          <span class="cat-item-name">06.03 Bag</span>
        </a>
        <div class="cat-item" style="opacity:0; pointer-events:none;"></div>
      </div>
    </div>
"""

def update_overlay(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    if 'id="catalogue-overlay"' not in content:
        return

    pattern = r'(<div id="catalogue-overlay">).*?(</div>\s*</div>)'
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, r'\1' + master_overlay_inner + r'\2', content, flags=re.DOTALL)
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated overlay in {filepath}")

files = [f for f in os.listdir('.') if f.endswith('.html') and f not in ['catalogue.html', 'index.html']]
for f in files:
    update_overlay(f)
