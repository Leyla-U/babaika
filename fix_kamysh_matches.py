import os

def fix_matches(filepath, matches):
    with open(filepath, 'r') as f:
        content = f.read()
    
    match_with_start = content.find('[ MATCH WITH ]')
    if match_with_start == -1: return
    
    # Find the container
    container_start = content.find('<div style="display: grid;', match_with_start)
    container_end = content.find('</div>\n</div>', container_start) + 7
    
    match_html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 32px;">'
    for m in matches:
        match_html += f"""
          <div onclick="window.location='{m['link']}'" style="cursor: pointer;">
            <img src="{m['img']}" style="width: 100%; aspect-ratio: 1; object-fit: cover; filter: brightness(0.96) saturate(0.9); transition: filter 0.3s;" onmouseover="this.style.filter='brightness(1) saturate(1)'" onmouseout="this.style.filter='brightness(0.96) saturate(0.9)'" />
            <p style="font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.15em; text-transform: uppercase; color: var(--text); margin-top: 16px;">{m['name']}</p>
            <p style="font-family: var(--font-mono); font-size: 11px; color: var(--text-faint);">{m['desc']}</p>
          </div>"""
    match_html += '\n        </div>'
    
    import re
    # We replace the whole inner grid
    pattern = r'<div style="display: grid; grid-template-columns: repeat\(auto-fit, minmax\(280px, 1fr\)\); gap: 32px;">.*?</div>\s*</div>'
    # Wait, the closing tags are tricky. Let's just find the next info-col end.
    
    new_content = content[:container_start] + match_html + content[container_end:]
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    print(f"Fixed matches in {filepath}")

beige = {'link': 'kamysh-kimono-beige.html', 'img': 'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777182352/kam11111_dfsfti.png', 'name': 'Kamýsh Kimono (Beige)', 'desc': 'Sand-washed satin silk'}
green = {'link': 'kamysh-kimono-green.html', 'img': 'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777182354/kam11111111_x4jeyl.png', 'name': 'Kamýsh Kimono (Grey-Green)', 'desc': 'Sand-washed satin silk'}
bag = {'link': 'kamysh-bag.html', 'img': 'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777184256/kambag_vyraac.png', 'name': 'Kamýsh Bag', 'desc': 'Silk dupioni'}

fix_matches('kamysh-kimono-beige.html', [green, bag])
fix_matches('kamysh-kimono-green.html', [beige, bag])
fix_matches('kamysh-bag.html', [beige, green])
