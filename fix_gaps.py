import os
import glob
import re

html_files = glob.glob('*.html')
for file in html_files:
    with open(file, 'r') as f:
        content = f.read()

    # Change .hero-video-grid gap: 2px to gap: 1px
    content = re.sub(r'(\.hero-video-grid\s*{[^}]*?gap:\s*)2px', r'\g<1>1px', content)
    
    # Change .hero-video-bottom gap: 2px to gap: 1px
    content = re.sub(r'(\.hero-video-bottom\s*{[^}]*?gap:\s*)2px', r'\g<1>1px', content)
    
    # In media query: .hero-video-grid, .hero-video-bottom, .image-strip, .image-strip-scroll, .artifact-grid, .kimono-grid { gap: 10px !important; }
    # Separate the photo/video ones out
    # Actually let's just replace the whole line if it matches
    old_line = r'\.hero-video-grid, \.hero-video-bottom, \.image-strip, \.image-strip-scroll, \.artifact-grid, \.kimono-grid \{ gap: 10px !important; \}'
    new_line = '.artifact-grid, .kimono-grid { gap: 10px !important; }\n      .hero-video-grid, .hero-video-bottom, .image-strip, .image-strip-scroll { gap: 1px !important; }'
    content = re.sub(old_line, new_line, content)
    
    # Also sometimes: .hero-video-grid { \n width: 100vw; gap: 10px; \n }
    content = re.sub(r'(\.hero-video-grid\s*\{\s*width:\s*100vw;\s*gap:\s*)10px(;?\s*\})', r'\g<1>1px\g<2>', content)

    # Some photo sliders or vertical galleries? 
    # "on videos or photos rows make sure we have 1px spacing vertically and horizontally"
    # let's write changes
    with open(file, 'w') as f:
        f.write(content)
print("Done")
