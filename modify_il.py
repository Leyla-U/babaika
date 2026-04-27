import re

def update_il_kimono():
    with open('il-kimono.html', 'r') as f:
        content = f.read()
    
    # Title and descriptions
    content = content.replace('<title>Babaika — Polói Kimono</title>', '<title>Babaika — Il Kimono</title>')
    content = content.replace('Chapter 01: Tuman', 'Chapter 04: Il')
    content = content.replace('Polói Kimono', 'Il Kimono')
    content = content.replace('[ TEXTILE ARTIFACT 03.01 ]', '[ TEXTILE ARTIFACT 04.01 ]')
    content = content.replace('Material: Blue chiffon silk', 'Concept: The Yielding Drape<br><br>Material: Brown-grey velvet.')
    content = content.replace('Selected for its weightless transparency. When worn, the blue chiffon functions exactly as the polói water does—as a thin, fluid layer that covers the body in the color of the reflected sky.', 'Translates the highly soft, saturated variation of the silt. The velvet is deeply opaque and lacks structural memory, melting against the body in a heavy, enveloping drape to capture the sudden, yielding softness of the mud.')
    
    # Stripe buttons
    content = re.sub(
        r'data-id="03\.01" data-price-id="[^"]+" data-name="Polói — Kimono" data-desc="Blue chiffon silk"',
        'data-id="04.01" data-price-id="price_1TQbXMJPn6LmQgwJn3zZwNpx" data-name="Il — Kimono" data-desc="Brown-grey velvet."',
        content
    )
    
    # Gallery ID
    content = content.replace('poloi_kimono_chiffon', 'il_kimono')
    
    # Replace the thumb-strip content
    gallery_html = """
        <div class="thumb-strip vertical-gallery" data-thumbs="il_kimono">
          <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777182384/il111111_ft12bx.png" alt="" />
          <video src="https://res.cloudinary.com/dejpm4v8y/video/upload/v1777172873/il-8_k4sfnf.mp4" autoplay loop muted playsinline></video>
          <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777177566/SHE00384_jplxeg.png" alt="" />
          <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777177561/SHE00373_iyfe5x.png" alt="" />
          <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777177562/SHE00380_xozzjn.png" alt="" />
          <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777177559/SHE00335_yacefv.png" alt="" />
          <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173455/babaika_il_53_zjtl1v.jpg" alt="" />
          <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173415/babaika_il_08_edvwxf.jpg" alt="" />
          <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173414/babaika_il_05_rsiwpg.jpg" alt="" />
          
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777177560/SHE00346_zka8xo.png" alt="" />
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777177564/SHE00392_c7wpol.png" alt="" />
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777182376/il111_twxmxj.png" alt="" />
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173452/babaika_il_41_nynut6.jpg" alt="" />
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173453/babaika_il_46_p2fpoh.jpg" alt="" />
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173454/babaika_il_49_u1xwcs.jpg" alt="" />
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173419/babaika_il_28_ysz5n8.jpg" alt="" />
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173418/babaika_il_27_ixunfj.jpg" alt="" />
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173417/babaika_il_22_le3hkb.jpg" alt="" />
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173416/babaika_il_13_b2a2bi.jpg" alt="" />
          <video class="hidden" src="https://res.cloudinary.com/dejpm4v8y/video/upload/v1777172866/il-4_e2xwiw.mp4" autoplay loop muted playsinline></video>
          <video class="hidden" src="https://res.cloudinary.com/dejpm4v8y/video/upload/v1777172869/il-5_lxfhva.mp4" autoplay loop muted playsinline></video>
        </div>"""
    
    # Use regex to replace the old vertical-gallery
    content = re.sub(
        r'<div class="thumb-strip vertical-gallery" data-thumbs="poloi_kimono_chiffon">.*?</div>',
        gallery_html,
        content,
        flags=re.DOTALL
    )
    
    # Match With Section
    match_with = """<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 32px; justify-content: center;">
        <div style="cursor: pointer;" onclick="window.location='il-ring.html'">
          <video src="https://res.cloudinary.com/dejpm4v8y/video/upload/v1777085494/il-ring_lpipgo.mp4" style="width: 100%; aspect-ratio: 1; object-fit: cover; filter: brightness(0.96) saturate(0.9); transition: filter 0.3s;" onmouseover="this.style.filter='brightness(1) saturate(1)'" onmouseout="this.style.filter='brightness(0.96) saturate(0.9)'" autoplay loop muted playsinline></video>
          <p style="font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.15em; text-transform: uppercase; color: var(--text); margin-top: 16px;">Il Ring</p>
          <p style="font-family: var(--font-mono); font-size: 11px; color: var(--text-faint);">Melted silver.</p>
        </div>
      </div>"""
      
    content = re.sub(
        r'<div style="display: grid; grid-template-columns: repeat\(auto-fit, minmax\(280px, 1fr\)\); gap: 32px;">.*?</div>\s*</div>',
        match_with + '\n    </div>',
        content,
        flags=re.DOTALL
    )
    
    # Explore Chapter Section
    content = content.replace('[ EXPLORE CHAPTER 03 ]', '[ EXPLORE CHAPTER 04 ]')
    content = content.replace('Polói', 'Il')
    content = content.replace("window.location='poloi.html'", "window.location='il.html'")
    
    with open('il-kimono.html', 'w') as f:
        f.write(content)

def update_il_ring():
    with open('il-ring.html', 'r') as f:
        content = f.read()
    
    content = content.replace('<title>Babaika — Tuman Ring</title>', '<title>Babaika — Il Ring</title>')
    content = content.replace('Tuman Ring', 'Il Ring')
    content = content.replace('[ HARDWARE ARTIFACT 01.02 ]', '[ HARDWARE ARTIFACT 04.02 ]')
    
    content = content.replace('Concept: Water memory mapping', 'Concept: The Compacted Sediment')
    content = content.replace('Material: Cast silver', 'Material: Melted silver.')
    
    # Old translation note was something else. Wait, let's find the exact string.
    # Tuman Ring has "The silver is cast to trace the organic imperfections of the shoreline..."
    # Actually, let's just use regex for the translation note.
    content = re.sub(
        r'(<strong[^>]*>\[ TRANSLATION NOTE \]</strong><br><br>\s*)(.*?)(?=\s*</p>)',
        r'\1Represents the heavier, compacted variation of silt—the rare form dense enough to build castles on the shore. The silver avoids looking traditionally cast; instead, it holds a heavier, deliberate shape, gripping the stone with the structural memory of dense, wet sediment.',
        content,
        flags=re.DOTALL
    )
    
    # Buttons
    content = re.sub(
        r'data-id="01\.02" data-price-id="[^"]+" data-name="Tuman — Ring" data-desc="Cast silver"',
        'data-id="04.02" data-price-id="price_1TQbZ1JPn6LmQgwJE9rPJZwV" data-name="Il — Ring" data-desc="Melted silver."',
        content
    )
    
    # Gallery
    content = content.replace('tuman_ring', 'il_ring')
    gallery_html = """
        <div class="thumb-strip vertical-gallery" data-thumbs="il_ring">
          <video src="https://res.cloudinary.com/dejpm4v8y/video/upload/v1777085494/il-ring_lpipgo.mp4" autoplay loop muted playsinline></video>
          <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777177651/de22_tvc9oz.png" alt="" />
        </div>"""
    
    content = re.sub(
        r'<div class="thumb-strip vertical-gallery" data-thumbs="il_ring">.*?</div>',
        gallery_html,
        content,
        flags=re.DOTALL
    )
    
    # Match with section
    match_with = """<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 32px; justify-content: center;">
        <div style="cursor: pointer;" onclick="window.location='il-kimono.html'">
          <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777182384/il111111_ft12bx.png" style="width: 100%; aspect-ratio: 1; object-fit: cover; filter: brightness(0.96) saturate(0.9); transition: filter 0.3s;" onmouseover="this.style.filter='brightness(1) saturate(1)'" onmouseout="this.style.filter='brightness(0.96) saturate(0.9)'" />
          <p style="font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.15em; text-transform: uppercase; color: var(--text); margin-top: 16px;">Il Kimono</p>
          <p style="font-family: var(--font-mono); font-size: 11px; color: var(--text-faint);">Brown-grey velvet.</p>
        </div>
      </div>"""
      
    content = re.sub(
        r'<div style="display: grid; grid-template-columns: repeat\(auto-fit, minmax\(280px, 1fr\)\); gap: 32px;">.*?</div>\s*</div>',
        match_with + '\n    </div>',
        content,
        flags=re.DOTALL
    )
    
    # Explore Chapter Section
    content = content.replace('[ EXPLORE CHAPTER 01 ]', '[ EXPLORE CHAPTER 04 ]')
    content = content.replace('Tuman', 'Il')
    content = content.replace("window.location='tuman.html'", "window.location='il.html'")
    
    with open('il-ring.html', 'w') as f:
        f.write(content)

update_il_kimono()
update_il_ring()
