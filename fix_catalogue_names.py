import os
import re

directory = '.'

NOMENCLATURE = {
    'tuman-kimono.html': '01.01 Kimono',
    'tuman-bra.html': '01.02 Bra',
    'tuman-ring.html': '01.03 Ring',
    'tuman-earring.html': '01.04 Earring',
    'tamarisk-kimono.html': '02.01 Kimono',
    'tamarisk-bra.html': '02.02 Bra',
    'tamarisk-ring.html': '02.03 Ring',
    'tamarisk-scarf.html': '02.04 Scarf',
    'poloi-kimono.html': '03.01 Kimono',
    'poloi-kimono-cotton.html': '03.02 Kimono',
    'poloi-bra.html': '03.03 Bra',
    'poloi-ring.html': '03.05 Ring',
    'il-kimono.html': '04.01 Kimono',
    'il-ring.html': '04.02 Ring',
    'raskaty-kimono.html': '05.01 Kimono',
    'raskaty-stockings.html': '05.02 The Navigational Seam',
    'raskaty-ring.html': '05.03 The Navigational Route',
    'kamish-kimono-beige.html': '06.01 Kimono',
    'kamish-kimono-green.html': '06.02 Kimono',
    'kamish-bag.html': '06.03 Bag',
    'kamish.html': '06.04 Belt',
    'cheshuya-bra.html': '07.01 Bra',
    'cheshuya-necklace.html': '07.02 Necklace',
    'cheshuya-necklace-2.html': '07.03 Necklace',
    'cheshuya-belt.html': '07.04 Belt'
}

for filename in os.listdir(directory):
    if not filename.endswith('.html'):
        continue
        
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r') as f:
        content = f.read()

    new_content = content

    for target_file, correct_name in NOMENCLATURE.items():
        # Match <a href="target_file" ... <span class="cat-item-name">OLD_NAME</span>
        # We need to be careful with multi-line matching.
        # Let's replace instances of <a href="target_file" class="cat-item">...<span class="cat-item-name">OLD</span>
        
        pattern = re.compile(
            rf'(<a\s+href="{re.escape(target_file)}"[^>]*>.*?<span\s+class="cat-item-name"[^>]*>)(.*?)(</span>)',
            re.DOTALL
        )
        new_content = pattern.sub(rf'\1{correct_name}\3', new_content)

    if content != new_content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated catalogue names in {filename}")

