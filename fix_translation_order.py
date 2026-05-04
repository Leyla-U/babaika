#!/usr/bin/env python3
"""
Move the translation IIFE to BEFORE the Lucide CDN script on all pages.
This ensures window.setLang is always defined regardless of CDN availability.
"""

import re, os, glob

BASE = '/Users/leylaudimamedova/babaika'
pages = glob.glob(os.path.join(BASE, '*.html'))
changed = []

for path in pages:
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html

    # Find the Lucide CDN script tag position
    lucide_pattern = re.compile(r'(\s*<!-- Lucide Icons -->.*?</script>\s*)', re.DOTALL)
    
    # Find the translation IIFE block
    # Match: <!-- ... TRANSLATION SYSTEM ... -->\n  <script>\n  (function() { ... })();\n  </script>
    trans_pattern = re.compile(
        r'(\s*<!-- [─\-]* TRANSLATION SYSTEM [─\-]* ?-->\s*<script>.*?\(function\(\).*?\}\)\(\);.*?</script>)',
        re.DOTALL
    )

    lucide_match = lucide_pattern.search(html)
    trans_match = trans_pattern.search(html)

    if not lucide_match or not trans_match:
        print(f'  skip (pattern not found): {os.path.basename(path)}')
        continue

    lucide_start = lucide_match.start()
    trans_start = trans_match.start()

    # Only move if translation is AFTER Lucide
    if trans_start <= lucide_start:
        print(f'  ok (already before Lucide): {os.path.basename(path)}')
        continue

    # Extract both blocks
    trans_block = trans_match.group(1)
    lucide_block = lucide_match.group(1)

    # Remove translation block from its current position
    html_no_trans = html[:trans_match.start()] + html[trans_match.end():]
    
    # Find Lucide in the modified html (position might shift slightly)
    lucide_match2 = lucide_pattern.search(html_no_trans)
    if not lucide_match2:
        print(f'  skip (lucide not found after removal): {os.path.basename(path)}')
        continue

    # Insert translation block BEFORE Lucide
    insert_pos = lucide_match2.start()
    html_fixed = html_no_trans[:insert_pos] + trans_block + html_no_trans[insert_pos:]

    if html_fixed != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html_fixed)
        changed.append(os.path.basename(path))
        print(f'  FIXED: {os.path.basename(path)}')
    else:
        print(f'  unchanged: {os.path.basename(path)}')

print(f'\nDone. Fixed {len(changed)} files.')
print('Changed:', changed)
