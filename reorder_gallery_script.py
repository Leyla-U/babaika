import os
import re
from bs4 import BeautifulSoup

def reorder_gallery(filepath):
    with open(filepath, 'r') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Update CSS to hide hidden videos
    style_tags = soup.find_all('style')
    for style in style_tags:
        if style.string and '.thumb-strip img.hidden { display: none; }' in style.string:
            style.string = style.string.replace(
                '.thumb-strip img.hidden { display: none; }',
                '.thumb-strip img.hidden, .thumb-strip video.hidden { display: none; }'
            )
    
    # 2. Reorder gallery items
    galleries = soup.find_all('div', class_='vertical-gallery')
    for gallery in galleries:
        elements = [c for c in gallery.contents if hasattr(c, 'name') and c.name in ['img', 'video']]
        
        visible_imgs = [e for e in elements if e.name == 'img' and 'hidden' not in e.get('class', [])]
        visible_vids = [e for e in elements if e.name == 'video' and 'hidden' not in e.get('class', [])]
        hidden_imgs = [e for e in elements if e.name == 'img' and 'hidden' in e.get('class', [])]
        hidden_vids = [e for e in elements if e.name == 'video' and 'hidden' in e.get('class', [])]
        
        gallery.clear()
        
        for e in visible_imgs:
            gallery.append(e)
            gallery.append('\n          ')
        for e in visible_vids:
            gallery.append(e)
            gallery.append('\n          ')
        for e in hidden_imgs:
            gallery.append(e)
            gallery.append('\n          ')
        for e in hidden_vids:
            gallery.append(e)
            gallery.append('\n          ')

    with open(filepath, 'w') as f:
        f.write(str(soup))
    print(f"Reordered gallery in {filepath}")

# Broad filter for product pages
files = [f for f in os.listdir('.') if f.endswith('.html') and any(x in f for x in ['-kimono', '-bra', '-ring', '-earring', '-scarf', '-stockings', '-bag', '-belt'])]

for f in files:
    reorder_gallery(f)
