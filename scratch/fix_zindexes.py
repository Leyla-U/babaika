import glob
import re

for filepath in glob.glob("*.html"):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # We want to increase z-indexes of cart, checkout, success, catalogue
    
    # cart-sidebar
    content = re.sub(r'(#cart-sidebar\s*{[^}]*z-index:\s*)9000(;)', r'\g<1>19000\2', content)
    # cart-overlay
    content = re.sub(r'(#cart-overlay\s*{[^}]*z-index:\s*)8999(;)', r'\g<1>18999\2', content)
    
    # checkout-modal
    content = re.sub(r'(#checkout-modal\s*{[^}]*z-index:\s*)9500(;)', r'\g<1>19500\2', content)
    # checkout-modal-bg
    content = re.sub(r'(#checkout-modal-bg\s*{[^}]*z-index:\s*)9499(;)', r'\g<1>19499\2', content)
    
    # success-modal
    content = re.sub(r'(#success-modal\s*{[^}]*z-index:\s*)9600(;)', r'\g<1>19600\2', content)
    # success-modal-bg (just in case)
    content = re.sub(r'(#success-modal-bg\s*{[^}]*z-index:\s*)9599(;)', r'\g<1>19599\2', content)
    
    # grid-overlay (already 20000, so it's fine)
    # catalogue-overlay (already 20000, so it's fine)
    
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed z-indexes in {filepath}")
