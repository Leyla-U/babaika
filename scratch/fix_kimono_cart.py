import os
import glob
import re

def patch_cart(filepath):
    with open(filepath, 'r') as f:
        html = f.read()
        
    original = html
    
    # We want to replace:
    # const div = document.createElement('div');
    # div.className = 'cart-item';
    # div.innerHTML = `
    #   <div class="cart-item-header">
    #     <span class="cart-item-title">${getTranslation(item.name)}</span>
    
    replacement = """
        let dName = item.name.replace(/KIMONO/g, 'WRAP').replace(/Kimono/g, 'Wrap');
        let dDesc = item.desc.replace(/KIMONO/g, 'WRAP').replace(/Kimono/g, 'Wrap');
        
        let transName = getTranslation(dName);
        let transDesc = getTranslation(dDesc);
        
        // Fallback for extremely old cached cart items
        if (localStorage.getItem('babaika_lang') === 'es') {
            if (transDesc === dDesc) {
                transDesc = transDesc.replace(/Base:/gi, 'Base:')
                                     .replace(/Pile:/gi, 'Pelo:')
                                     .replace(/Mulberry Silk/gi, 'Seda de morera')
                                     .replace(/Rayon/gi, 'Rayón')
                                     .replace(/Cotton/gi, 'Algodón')
                                     .replace(/Silk Poplin/gi, 'Popelín de seda')
                                     .replace(/Chiffon silk/gi, 'Gasa de seda')
                                     .replace(/with rose pattern/gi, 'con patrón de rosas');
            }
        }

        const div = document.createElement('div');
        div.className = 'cart-item';
        div.innerHTML = `
          <div class="cart-item-header">
            <span class="cart-item-title">${transName}</span>
            <button class="cart-item-remove" data-idx="${idx}" aria-label="Remove">×</button>
          </div>
          <span class="cart-item-meta">${transDesc}</span>
"""
    
    # We use regex to find the block
    pattern = r'const div = document\.createElement\(\'div\'\);\s*div\.className = \'cart-item\';\s*div\.innerHTML = `\s*<div class="cart-item-header">\s*<span class="cart-item-title">\$\{getTranslation\(item\.name\)\}</span>\s*<button class="cart-item-remove" data-idx="\$\{idx\}" aria-label="Remove">×</button>\s*</div>\s*<span class="cart-item-meta">\$\{getTranslation\(item\.desc\)\}</span>'
    
    html = re.sub(pattern, replacement.strip(), html)
    
    if html != original:
        with open(filepath, 'w') as f:
            f.write(html)
        print(f"Patched cart in {filepath}")

for f in glob.glob("*.html"):
    if not f.startswith("index_") and not f.startswith("about_"):
        patch_cart(f)
