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
    'kamish.html': '$2,600.00 MXN' 
}

chapter_files = ['tuman.html', 'tamarisk.html', 'poloi.html', 'il.html', 'raskaty.html', 'kamish.html', 'cheshuya.html']

def insert_prices_in_chapter(content):
    pattern = re.compile(r'(<div class="artifact-actions"[\s\S]*?window\.location=\'(.*?)\'[\s\S]*?</button>\n*\s*</div>)')
    
    matches = pattern.findall(content)
    for match, url in matches:
        if url in file_to_price:
            price = file_to_price[url]
            price_tag = f'<p class="artifact-detail-row" style="margin-top:8px;">Price: {price}</p>'
            
            # Check if this specific match already has the price right before it
            if content.find(price_tag + '\n        ' + match) != -1:
                continue
                
            content = content.replace(match, price_tag + '\n        ' + match)
    return content

for f in chapter_files:
    with open(f, 'r') as file:
        content = file.read()
    new_content = insert_prices_in_chapter(content)
    if new_content != content:
        with open(f, 'w') as file:
            file.write(new_content)
        print(f"Updated {f}")

