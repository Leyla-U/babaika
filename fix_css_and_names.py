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

    # 1. Fix CSS margin-bottom for padding under texts
    new_content = new_content.replace(
        "margin: 32px auto 0 !important;",
        "margin: 32px auto 64px !important;"
    )

    # 2. Fix double line by adding .info-col:last-child { border-bottom: none !important; }
    if ".info-col { border-right: none !important; border-bottom: 1px solid var(--line) !important; padding: 40px 24px !important; }" in new_content:
        if ".info-col:last-child" not in new_content:
            new_content = new_content.replace(
                ".info-col { border-right: none !important; border-bottom: 1px solid var(--line) !important; padding: 40px 24px !important; }",
                ".info-col { border-right: none !important; border-bottom: 1px solid var(--line) !important; padding: 40px 24px !important; }\n      .info-col:last-child { border-bottom: none !important; }"
            )

    # 3. Update artifact name if it's in NOMENCLATURE
    if filename in NOMENCLATURE:
        correct_name = NOMENCLATURE[filename]
        # Replace the h1 content
        new_content = re.sub(
            r'(<h1 class="artifact-name"[^>]*>)[^<]+(</h1>)',
            rf'\g<1>{correct_name}\g<2>',
            new_content
        )
        
        # 4. Swap h1 and p.artifact-tag order by parsing
        # Find the h1 and the p tag and swap them if h1 comes before p
        match = re.search(r'(<h1 class="artifact-name"[^>]*>.*?</h1>)\s*(<p class="artifact-tag"[^>]*>.*?</p>)', new_content, re.DOTALL)
        if match:
            h1_tag = match.group(1)
            p_tag = match.group(2)
            # Make sure to keep the title (tag) above the object name (h1)
            # But the user specifically asked for mobile. If we swap them in HTML, it changes desktop too.
            # Let's wrap them in a flex div that reverses order ONLY on mobile.
            if "artifact-title-group" not in new_content:
                wrapped = f'<div class="artifact-title-group">\n{h1_tag}\n{p_tag}\n</div>'
                new_content = new_content.replace(match.group(0), wrapped)
                
                # inject CSS for artifact-title-group
                css_to_add = """
    @media (max-width: 768px) {
      .artifact-title-group { display: flex; flex-direction: column; }
      .artifact-title-group .artifact-tag { order: 1; margin-bottom: 8px !important; margin-top: 0 !important; }
      .artifact-title-group .artifact-name { order: 2; margin-top: 0 !important; }
    }
"""
                if "</style>" in new_content:
                    new_content = new_content.replace("</style>", css_to_add + "</style>")

    if content != new_content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated {filename}")

