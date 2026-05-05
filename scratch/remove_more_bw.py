import os
import glob
import re

def remove_more_bw(filepath):
    with open(filepath, 'r') as f:
        html = f.read()
    original = html
    
    # We want to remove specific B&W photos and videos from the thumb-strip
    bw_patterns = [
        r'raskaty_mztszb\.png',
        r'raskty3_len1k6\.png',
        r'tuman-6_grktcd\.mp4',
        r'te1_kjzxym\.png' # just in case
    ]
    
    def replace_in_thumb_strip(m):
        block = m.group(0)
        # remove any <img> or <video> containing these strings
        for pat in bw_patterns:
            block = re.sub(r'<(img|video)[^>]*' + pat + r'[^>]*>\s*</video>\s*', '', block)
            block = re.sub(r'<(img|video)[^>]*' + pat + r'[^>]*>\s*', '', block)
        return block

    html = re.sub(r'<div class="thumb-strip[^>]*>.*?</div>', replace_in_thumb_strip, html, flags=re.DOTALL)
    
    if html != original:
        with open(filepath, 'w') as f:
            f.write(html)
        print(f"Removed more BW from gallery in {filepath}")

chapters = ['tuman.html', 'tamarisk.html', 'poloi.html', 'il.html', 'raskaty.html', 'kamish.html', 'cheshuya.html']
for f in glob.glob("*.html"):
    if f.startswith("index") or f.startswith("about") or f.startswith("catalogue"):
        continue
    if f in chapters:
        continue
    
    remove_more_bw(f)
