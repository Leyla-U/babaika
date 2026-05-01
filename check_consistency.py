import glob
import re

# Source of truth from catalogue
products = {
    "tuman-kimono.html":       {"price": "$6,000.00 MXN", "material": "Mulberry Silk and Rayon Velvet"},
    "tuman-bra.html":          {"price": "$2,000.00 MXN", "material": "Mulberry Silk Chiffon 8 Momme"},
    "tuman-earring.html":      {"price": "$800.00 MXN",   "material": "Silver, River Pearls"},
    "tuman-ring.html":         {"price": "$1,600.00 MXN", "material": "Silver, River Pearls"},
    "tamarisk-kimono.html":    {"price": "$4,000.00 MXN", "material": "Mulberry Silk 6 Momme Georgette"},
    "tamarisk-bra.html":       {"price": "$2,000.00 MXN", "material": "Mulberry Silk 6 Momme Georgette"},
    "tamarisk-ring.html":      {"price": "$1,600.00 MXN", "material": "Silver, Lab Grown Rubies"},
    "poloi-kimono.html":       {"price": "$6,000.00 MXN", "material": "Mulberry Silk Chiffon 8 Momme"},
    "poloi-bra.html":          {"price": "$2,000.00 MXN", "material": "Mulberry Silk Chiffon 8 Momme"},
    "poloi-ring.html":         {"price": "$1,600.00 MXN", "material": "Silver"},
    "poloi-kimono-cotton.html":{"price": "$6,000.00 MXN", "material": "50% Silk, 50% Cotton Poplin"},
    "il-kimono.html":          {"price": "$6,000.00 MXN", "material": "Mulberry Silk and Rayon Velvet"},
    "il-ring.html":            {"price": "$800.00 MXN",   "material": "Silver"},
    "raskaty-kimono.html":     {"price": "$4,000.00 MXN", "material": "Synthetic Pleated Chiffon"},
    "raskaty-stockings.html":  {"price": "$1,000.00 MXN", "material": "Nylon Mesh"},
    "raskaty-ring.html":       {"price": "$1,600.00 MXN", "material": "Silver, Moissanite"},
    "kamish-kimono-beige.html":{"price": "$6,000.00 MXN", "material": "Sandwashed Mulberry Silk Charmeuse 16 Momme"},
    "kamish-kimono-green.html":{"price": "$6,000.00 MXN", "material": "Sandwashed Mulberry Silk Charmeuse 16 Momme"},
    "kamish-bag.html":         {"price": "$2,600.00 MXN", "material": "Mulberry Silk Dupioni"},
    "cheshuya-bra.html":       {"price": "$2,000.00 MXN", "material": "50% Silk, 50% Cotton Charmeuse Base, Motherpearl Shell Coins"},
    "cheshuya-necklace.html":  {"price": "$2,600.00 MXN", "material": "50% Silk, 50% Cotton Charmeuse Base, Motherpearl Shell Coins"},
    "cheshuya-necklace-2.html":{"price": "$1,600.00 MXN", "material": "Motherpearl Shells"},
    "cheshuya-belt.html":      {"price": "$1,600.00 MXN", "material": "Motherpearl Shells"},
}

for fname, data in products.items():
    try:
        with open(fname, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"NOT FOUND: {fname}")
        continue

    price = data["price"]
    if "Price: " + price not in content:
        cur_prices = re.findall(r"Price: \$[\d,]+\.\d+ MXN", content)
        print(f"PRICE MISMATCH in {fname}: expected '{price}', found {cur_prices}")

    mat = data["material"]
    if mat not in content:
        cur_desc = re.findall(r'data-desc="([^"]+)"', content)
        print(f"MATERIAL MISMATCH in {fname}: expected '{mat}'")
        print(f"  -> found data-desc={cur_desc}")
