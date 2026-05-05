import os
import glob
import re

def remove_bw_from_gallery(filepath):
    with open(filepath, 'r') as f:
        html = f.read()
    original = html
    
    # We want to remove any <img> tag that contains "babaika_film" OR "babaika_delta"
    # ONLY if it's inside <div class="thumb-strip ..."> ... </div>
    
    def replace_in_thumb_strip(m):
        block = m.group(0)
        # remove any <img> containing babaika_film or babaika_delta
        new_block = re.sub(r'<img[^>]*(babaika_film|babaika_delta)[^>]*>\s*', '', block)
        return new_block

    html = re.sub(r'<div class="thumb-strip[^>]*>.*?</div>', replace_in_thumb_strip, html, flags=re.DOTALL)
    
    if html != original:
        with open(filepath, 'w') as f:
            f.write(html)
        print(f"Removed BW from gallery in {filepath}")

chapters = ['tuman.html', 'tamarisk.html', 'poloi.html', 'il.html', 'raskaty.html', 'kamish.html', 'cheshuya.html']
for f in glob.glob("*.html"):
    if f.startswith("index") or f.startswith("about") or f.startswith("catalogue"):
        continue
    if f in chapters:
        continue
    
    remove_bw_from_gallery(f)
