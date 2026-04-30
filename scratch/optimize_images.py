import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

# We'll use a regex to find all <img ... > tags
img_pattern = re.compile(r'(<img\s+[^>]+>)', re.IGNORECASE)

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original_content = content
    
    # --- STEP 1: Cloudinary q_auto,f_auto ---
    # First, let's normalize by removing existing q_auto,f_auto if they are immediately after upload/
    content = content.replace('image/upload/q_auto,f_auto/', 'image/upload/')
    # Now, add it to all image/upload/
    content = content.replace('image/upload/', 'image/upload/q_auto,f_auto/')
    
    # --- STEP 2: Lazy Loading ---
    def add_lazy_loading(match):
        img_tag = match.group(1)
        
        # Don't add lazy loading if it's already there
        if 'loading=' in img_tag.lower():
            return img_tag
            
        # Optional: We could skip 'main-photo' to keep Largest Contentful Paint (LCP) fast
        if 'class="main-photo"' in img_tag or "class='main-photo'" in img_tag:
            return img_tag
            
        # Insert loading="lazy" before the closing bracket
        if img_tag.endswith('/>'):
            return img_tag[:-2] + ' loading="lazy" />'
        elif img_tag.endswith('>'):
            return img_tag[:-1] + ' loading="lazy">'
        return img_tag

    # Apply the lazy loading transformation
    content = img_pattern.sub(add_lazy_loading, content)
    
    # Write back if changed
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Optimized: {filepath}")

print("Optimization complete!")
