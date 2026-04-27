import os
import re

# Files to exclude from renaming
EXCLUDE_FILES = ['index.html']

# Directory to process
directory = '.'

# Mapping of product files to their new Title Case names
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
    if not filename.endswith('.html') or filename in EXCLUDE_FILES:
        continue
        
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r') as f:
        content = f.read()

    new_content = content

    for target_file, correct_name in NOMENCLATURE.items():
        # 1. Update <h1 class="artifact-name"> (Product pages)
        # It's currently e.g. 01.01 Kimono, we replace with correct_name
        # Note: We only do this if it's the exact target file
        if filename == target_file:
            pattern_h1 = re.compile(r'(<h1 class="artifact-name"[^>]*>)[^<]+(</h1>)')
            new_content = pattern_h1.sub(rf'\g<1>{correct_name}\g<2>', new_content)
        
        # 2. Update MATCH WITH references
        pattern_match = re.compile(
            rf'(<div\s+onclick="window\.location=\'{re.escape(target_file)}\'"[^>]*>.*?<p[^>]*style="[^"]*font-size:\s*11px[^"]*"[^>]*>)(.*?)(</p>)',
            re.DOTALL | re.IGNORECASE
        )
        new_content = pattern_match.sub(rf'\1{correct_name}\3', new_content)
        
        # 3. Update catalogue spans: <a href="target_file" ... <span class="cat-item-name">OLD</span>
        pattern_cat = re.compile(
            rf'(<a\s+href="{re.escape(target_file)}"[^>]*>.*?<span\s+class="cat-item-name"[^>]*>)(.*?)(</span>)',
            re.DOTALL
        )
        new_content = pattern_cat.sub(rf'\1{correct_name}\3', new_content)

        # 4. Update chapter pages: <div class="artifact-item" onclick="window.location='target_file'"> <p class="artifact-title">01.01 KIMONO</p>
        upper_name = correct_name.upper()
        pattern_chapter_list = re.compile(
            rf'(<div class="artifact-item" onclick="window\.location=\'{re.escape(target_file)}\'">\s*<p class="artifact-title">)[^<]+(</p>)',
            re.DOTALL
        )
        new_content = pattern_chapter_list.sub(rf'\g<1>{upper_name}\g<2>', new_content)

        # 5. Update chapter pages artifact blocks:
        # <div class="artifact-left" onclick="window.location='target_file'"> <p class="artifact-name">KIMONO</p>
        # Note: correct_name looks like "01.01 Velvet Kimono", but in chapter artifact blocks they usually don't have the 01.01 prefix.
        # However, it's better to extract the name part. Let's strip the number part.
        short_name = re.sub(r'^\d+\.\d+\s+', '', correct_name).upper()
        pattern_chapter_block = re.compile(
            rf'(<div class="artifact-left" onclick="window\.location=\'{re.escape(target_file)}\'">\s*<p class="artifact-name">)[^<]+(</p>)',
            re.DOTALL
        )
        new_content = pattern_chapter_block.sub(rf'\g<1>{short_name}\g<2>', new_content)


    if content != new_content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated names in {filename}")

