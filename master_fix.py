import os
import re

directory = '.'

NOMENCLATURE = {
    'tuman-kimono.html': '01.01 Velvet Kimono',
    'tuman-bra.html': '01.02 Chiffon Bra',
    'tamarisk-kimono.html': '02.01 Chiffon Kimono',
    'tamarisk-bra.html': '02.02 Chiffon Bra',
    'poloi-kimono.html': '03.01 Chiffon Kimono',
    'poloi-bra.html': '03.03 Chiffon Bra',
    'il-kimono.html': '04.01 Velvet Kimono',
    'kamish-kimono-beige.html': '06.01 Sandwashed Charmeuse Kimono',
    'kamish-kimono-green.html': '06.02 Sandwashed Charmeuse Kimono',
    'cheshuya-bra.html': '07.01 Shell Bra',
    'cheshuya-necklace.html': '07.02 Shell Necklace',
    'cheshuya-necklace-2.html': '07.03 Shell Necklace',
    'cheshuya-belt.html': '07.04 Shell Belt'
}

for filename in os.listdir(directory):
    if not filename.endswith('.html'):
        continue

    filepath = os.path.join(directory, filename)
    with open(filepath, 'r') as f:
        content = f.read()
    new_content = content

    # 1. Remove Inquire / Inquiry Buttons
    # Pattern to find any button with "Inquiry" or "Inquire"
    new_content = re.sub(r'<button[^>]*>Inquire</button>\s*', '', new_content, flags=re.IGNORECASE)
    new_content = re.sub(r'<button[^>]*>Inquiry</button>\s*', '', new_content, flags=re.IGNORECASE)
    
    # Also remove "Buy Now" since previous script might have replaced them? Actually I don't know if buy now was there.

    # 2. Fix Double Lines
    target_double = ".info-col { border-right: none !important; border-bottom: 1px solid var(--line) !important; padding: 40px 24px !important; }"
    replacement_double = target_double + "\n      .info-col:last-child { border-bottom: none !important; }"
    if target_double in new_content and replacement_double not in new_content:
        new_content = new_content.replace(target_double, replacement_double)

    # 3. Mobile padding fix on product pages
    new_content = new_content.replace("margin: 32px auto 0 !important;", "margin: 32px auto 64px !important;")

    # 4. Cheshuya drawing removal & hero videos
    if filename == 'cheshuya.html':
        # Remove drawing div
        pattern_drawing = re.compile(r'<div style="margin-top: 40px; width: 100%;">\s*<img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777264681/Group_14_yvv1cv.png"[^>]*>\s*</div>', re.DOTALL)
        new_content = pattern_drawing.sub('', new_content)
        
        # Update three media assets
        old_hero_bottom = r"""      <div class="hero-video-bottom">
        <video preload="none" src="https://res.cloudinary.com/dejpm4v8y/video/upload/q_auto,f_auto,vc_auto/v1777053278/cheshuya_xrwr2l.mp4" autoplay loop muted playsinline></video>
        <video preload="none" src="https://res.cloudinary.com/dejpm4v8y/video/upload/q_auto,f_auto,vc_auto/v1777053278/cheshuya_xrwr2l.mp4" autoplay loop muted playsinline></video>
        <video preload="none" src="https://res.cloudinary.com/dejpm4v8y/video/upload/q_auto,f_auto,vc_auto/v1777053278/cheshuya_xrwr2l.mp4" autoplay loop muted playsinline></video>
      </div>"""
        new_hero_bottom = """      <div class="hero-video-bottom">
        <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777256321/hesh-tits_gnsgol.png" alt="Cheshuya detail" />
        <video preload="none" src="https://res.cloudinary.com/dejpm4v8y/video/upload/v1777083709/cheshuya-material_d7rghf.mp4" autoplay loop muted playsinline></video>
        <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777256346/a5d46c29a1180e7f9855aa76d1e125ff_vvnezs.jpg" alt="Cheshuya detail" />
      </div>"""
        if old_hero_bottom in new_content:
            new_content = new_content.replace(old_hero_bottom, new_hero_bottom)

    # 5. About page mobile padding
    if filename == 'about.html':
        new_content = new_content.replace("main { padding: 0 75px; margin: 80px auto; }", "main { padding: 0 24px; margin: 80px auto; }")

    # 6. index.html transcriptions
    if filename == 'index.html':
        transcriptions = {
            'ТАМАРИСК • Tamarisk': 'ТАМАРИСК • Tamarisk [ta-ma-ˈrisk]',
            'ПОЛОИ • Poloi': 'ПОЛОИ • Polói [pa-ˈlo-ee]',
            'ИЛ • Il': 'ИЛ • Il [eel]',
            'РАСКАТЫ • Raskaty': 'РАСКАТЫ • Raskáty [ras-ˈka-ti]',
            'КАМЫШ • Kamish': 'КАМЫШ • Kamish [ka-ˈmish]',
            'ЧЕШУЯ • Cheshuya': 'ЧЕШУЯ • Cheshuyá [che-shu-ˈya]'
        }
        for original, transcribed in transcriptions.items():
            pattern_tr = re.compile(rf'(<p class="chapter-label"[^>]*>){original}(</p>)')
            new_content = pattern_tr.sub(rf'\g<1>{transcribed}\g<2>', new_content)

    # 7. Tamarisk drawing URL update
    old_url = 'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777141533/tamarisk_drawing_pfoo89.png'
    new_url = 'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777253509/tamarisk_drawing_pfoo89.png'
    new_content = new_content.replace(old_url, new_url)

    # 8. Mobile artifact title fix (reversing h1 and p.artifact-tag)
    # But only if it has an h1 and p.artifact-tag
    if filename not in ['index.html', 'catalogue.html', 'about.html']:
        match = re.search(r'(<h1 class="artifact-name"[^>]*>.*?</h1>)\s*(<p class="artifact-tag"[^>]*>.*?</p>)', new_content, re.DOTALL)
        if match and "artifact-title-group" not in new_content:
            h1_tag = match.group(1)
            p_tag = match.group(2)
            wrapped = f'<div class="artifact-title-group">\n{h1_tag}\n{p_tag}\n</div>'
            new_content = new_content.replace(match.group(0), wrapped)
            
            css_to_add = """
    @media (max-width: 768px) {
      .artifact-title-group { display: flex; flex-direction: column; }
      .artifact-title-group .artifact-tag { order: 1; margin-bottom: 8px !important; margin-top: 0 !important; }
      .artifact-title-group .artifact-name { order: 2; margin-top: 0 !important; }
    }
"""
            if "</style>" in new_content and "artifact-title-group" not in new_content:
                new_content = new_content.replace("</style>", css_to_add + "</style>")

    # 9. Nomenclature Rename
    if filename != 'index.html':
        # Apply renaming rules
        for target_file, correct_name in NOMENCLATURE.items():
            # A) Update <h1 class="artifact-name"> on specific product pages
            if filename == target_file:
                pattern_h1 = re.compile(r'(<h1 class="artifact-name"[^>]*>)[^<]+(</h1>)')
                new_content = pattern_h1.sub(rf'\g<1>{correct_name}\g<2>', new_content)
            
            # B) Update MATCH WITH references
            pattern_match = re.compile(
                rf'(<div\s+onclick="window\.location=\'{re.escape(target_file)}\'"[^>]*>.*?<p[^>]*style="[^"]*font-size:\s*11px[^"]*"[^>]*>)(.*?)(</p>)',
                re.DOTALL | re.IGNORECASE
            )
            new_content = pattern_match.sub(rf'\g<1>{correct_name}\g<3>', new_content)
            
            # C) Update catalogue spans: <a href="target_file" ... <span class="cat-item-name">OLD</span>
            pattern_cat = re.compile(
                rf'(<a\s+href="{re.escape(target_file)}"[^>]*>.*?<span\s+class="cat-item-name"[^>]*>)(.*?)(</span>)',
                re.DOTALL
            )
            new_content = pattern_cat.sub(rf'\g<1>{correct_name}\g<3>', new_content)

            # D) Update catalogue spans without href but inside catalogue.html cat-item:
            # <div class="cat-item-thumb"><img.../></div> <span class="cat-item-name">OLD</span>
            # Wait, catalogue.html uses <a href="tuman-kimono.html" ... >
            # YES! I checked git diff, it uses <a href="tuman-kimono.html" class="cat-item">
            # So pattern_cat handles it perfectly, because I used \g<1> and \g<3> !

            # E) Update chapter pages: <div class="artifact-item" onclick="window.location='target_file'"> <p class="artifact-title">KIMONO</p>
            upper_name = correct_name.upper()
            pattern_chapter_list = re.compile(
                rf'(<div class="artifact-item" onclick="window\.location=\'{re.escape(target_file)}\'">\s*<p class="artifact-title">)[^<]+(</p>)',
                re.DOTALL
            )
            new_content = pattern_chapter_list.sub(rf'\g<1>{upper_name}\g<2>', new_content)

            # F) Update chapter pages artifact blocks:
            # <div class="artifact-left" onclick="window.location='target_file'"> <p class="artifact-name">KIMONO</p>
            short_name = re.sub(r'^\d+\.\d+\s+', '', correct_name).upper()
            pattern_chapter_block = re.compile(
                rf'(<div class="artifact-left" onclick="window\.location=\'{re.escape(target_file)}\'">\s*<p class="artifact-name">)[^<]+(</p>)',
                re.DOTALL
            )
            new_content = pattern_chapter_block.sub(rf'\g<1>{short_name}\g<2>', new_content)

    if content != new_content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Master script updated {filename}")

