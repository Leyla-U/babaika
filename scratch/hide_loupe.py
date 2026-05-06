import glob
import re

for filepath in glob.glob("*.html"):
    with open(filepath, 'r') as f:
        content = f.read()

    original = content
    
    # 1. Update openCart
    open_cart_pattern = r"function openCart\(\)\s*\{\s*cartSidebar\.classList\.add\('open'\);\s*cartOverlay\.classList\.add\('visible'\);\s*\}"
    open_cart_repl = """function openCart() {
      cartSidebar.classList.add('open');
      cartOverlay.classList.add('visible');
      document.body.classList.add('cart-open');
    }"""
    content = re.sub(open_cart_pattern, open_cart_repl, content)
    
    # 2. Update closeCart
    close_cart_pattern = r"function closeCart\(\)\s*\{\s*cartSidebar\.classList\.remove\('open'\);\s*cartOverlay\.classList\.remove\('visible'\);\s*\}"
    close_cart_repl = """function closeCart() {
      cartSidebar.classList.remove('open');
      cartOverlay.classList.remove('visible');
      document.body.classList.remove('cart-open');
    }"""
    content = re.sub(close_cart_pattern, close_cart_repl, content)

    # 3. Add CSS rule if not present
    if "body.cart-open #mag-cursor" not in content:
        content = content.replace("  </style>", "    body.cart-open #mag-cursor,\n    body.cart-open #mag-zoom {\n      display: none !important;\n    }\n  </style>")

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated cart magnifier logic in {filepath}")

