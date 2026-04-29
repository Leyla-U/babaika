import os
import re

file_to_price = {
    'tuman-kimono.html': '$6,000.00 MXN',
    'tuman-ring.html': '$1,600.00 MXN',
    'tuman-earring.html': '$800.00 MXN',
    'tuman-bra.html': '$2,000.00 MXN',
    'tamarisk-kimono.html': '$4,000.00 MXN',
    'tamarisk-bra.html': '$2,000.00 MXN',
    'tamarisk-ring.html': '$2,600.00 MXN',
    'poloi-kimono.html': '$4,000.00 MXN',
    'poloi-kimono-cotton.html': '$4,000.00 MXN',
    'poloi-bra.html': '$2,000.00 MXN',
    'poloi-ring.html': '$2,000.00 MXN',
    'il-kimono.html': '$6,000.00 MXN',
    'il-ring.html': '$2,000.00 MXN',
    'raskaty-kimono.html': '$4,000.00 MXN',
    'raskaty-stockings.html': '$1,000.00 MXN',
    'raskaty-ring.html': '$2,600.00 MXN',
    'kamish-kimono-beige.html': '$6,000.00 MXN',
    'kamish-kimono-green.html': '$6,000.00 MXN',
    'kamish-bag.html': '$2,600.00 MXN',
    'cheshuya-bra.html': '$4,000.00 MXN',
    'cheshuya-belt.html': '$1,600.00 MXN',
    'cheshuya-necklace.html': '$2,600.00 MXN',
    'cheshuya-necklace-2.html': '$1,600.00 MXN',
    # Adding kamish.html since kamish belt links to it
    'kamish.html': '$2,600.00 MXN' 
}

# Fix missing mapping: 02.03 Tamarisk Scarf maybe?
# The list: 02.03 Tamarisk Silver Ring with Lab Rubies $2,600.00 MXN.
# Wait, tamarisk ring with rubies is $2,600.00 MXN. `tamarisk-ring.html` -> $2,600.00 MXN. 
# Are there any others? What about tamarisk-scarf?
# The user's list does NOT have Tamarisk Scarf. It has 24 items.
# Let's count items in our list.
print(len(file_to_price) - 1)

# Directory iteration
html_files = [f for f in os.listdir('.') if f.endswith('.html')]

chapter_files = ['tuman.html', 'tamarisk.html', 'poloi.html', 'il.html', 'raskaty.html', 'kamish.html', 'cheshuya.html']
product_files = [f for f in html_files if f not in chapter_files and f != 'index.html' and f != 'about.html' and f != 'catalogue.html' and not f.endswith('_es.html') and not f.endswith('_ru.html')]

print("Product files:", product_files)

def insert_price_before_actions(content, filename):
    original = content
    # For product pages, there is exactly one <div class="artifact-actions"...> that corresponds to the product.
    if filename in file_to_price:
        price = file_to_price[filename]
        price_tag = f'<p class="artifact-detail-row" style="margin-top:8px;">Price: {price}</p>'
        
        # Avoid duplicate insertions
        if price_tag in content:
            return content
        
        # Replace the single artifact-actions block
        # We need to find the <div class="artifact-actions" block
        # Since product pages only have 1 (excluding possible catalogue overlays which don't have artifact-actions), 
        # we can just replace it.
        pattern = re.compile(r'(<div class="artifact-actions"[\s\S]*?>[\s\S]*?</button>\n*\s*</div>)')
        matches = pattern.findall(content)
        if len(matches) == 1:
            content = content.replace(matches[0], price_tag + '\n' + matches[0])
            
    return content

def insert_prices_in_chapter(content):
    # In chapter pages, there are multiple artifact-actions blocks, each containing a button with window.location='...'
    # We can match the window.location and insert the corresponding price before the div.
    pattern = re.compile(r'(<div class="artifact-actions"[\s\S]*?window\.location=\'(.*?)\'[\s\S]*?</button>\n*\s*</div>)')
    
    # Iterate over all matches
    matches = pattern.findall(content)
    for match, url in matches:
        if url in file_to_price:
            price = file_to_price[url]
            price_tag = f'<p class="artifact-detail-row" style="margin-top:8px;">Price: {price}</p>'
            
            if price_tag in content:
                continue
                
            content = content.replace(match, price_tag + '\n        ' + match)
    return content

for f in product_files:
    with open(f, 'r') as file:
        content = file.read()
    new_content = insert_price_before_actions(content, f)
    if new_content != content:
        with open(f, 'w') as file:
            file.write(new_content)
        print(f"Updated {f}")

for f in chapter_files:
    with open(f, 'r') as file:
        content = file.read()
    new_content = insert_prices_in_chapter(content)
    if new_content != content:
        with open(f, 'w') as file:
            file.write(new_content)
        print(f"Updated {f}")
