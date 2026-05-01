import re

fixes = {
    # file: list of (old, new) replacements
    "catalogue.html": [
        # Fix Tamarisk Bra image
        ('v1777167754/tmr123_mjl8ib.png', 'v1777224852/tmr12_jkch4z.png'),
        # Fix Kamish catalogue descs to match product pages
        ('Beige Sandwashed Silk Charmeuse 16 Momme', 'Beige Sandwashed Mulberry Silk Charmeuse 16 Momme'),
        ('Grey Green Sandwashed Silk Charmeuse 16 Momme', 'Grey Green Sandwashed Mulberry Silk Charmeuse 16 Momme'),
    ],

    "tuman-earring.html": [
        ('data-desc="Chapter 01"', 'data-desc="Silver, River Pearls"'),
    ],

    "tuman-ring.html": [
        ('data-desc="Silver"', 'data-desc="Silver, River Pearls"'),
        ('Material: Silver with Rhodium Plating', 'Material: Silver, River Pearls'),
    ],

    "tamarisk-kimono.html": [
        ('data-desc="Chiffon Silk with Rose Pattern"', 'data-desc="Mulberry Silk 6 Momme Georgette"'),
        ('Material: Chiffon Silk with Rose Pattern', 'Material: Mulberry Silk 6 Momme Georgette'),
    ],

    "tamarisk-bra.html": [
        ('data-desc="Chiffon Silk with Rose Pattern"', 'data-desc="Mulberry Silk 6 Momme Georgette"'),
        ('Material: Chiffon Silk with Rose Pattern', 'Material: Mulberry Silk 6 Momme Georgette'),
    ],

    "tamarisk-ring.html": [
        ('Price: $2,600.00 MXN', 'Price: $1,600.00 MXN'),
        ('data-desc="Silver, Rubies"', 'data-desc="Silver, Lab Grown Rubies"'),
        ('Material: Silver, Lab-Grown Rubies or Garnets', 'Material: Silver, Lab Grown Rubies'),
    ],

    "poloi-kimono.html": [
        ('Price: $4,000.00 MXN', 'Price: $6,000.00 MXN'),
    ],

    "poloi-ring.html": [
        ('Price: $2,000.00 MXN', 'Price: $1,600.00 MXN'),
    ],

    "poloi-kimono-cotton.html": [
        ('Price: $4,000.00 MXN', 'Price: $6,000.00 MXN'),
    ],

    "il-ring.html": [
        ('Price: $2,000.00 MXN', 'Price: $800.00 MXN'),
    ],

    "raskaty-ring.html": [
        ('Price: $2,600.00 MXN', 'Price: $1,600.00 MXN'),
        ('data-desc="Silver, 1mm Moissanite Line"', 'data-desc="Silver, Moissanite"'),
        ('Material: Silver, 1mm Moissanite Line', 'Material: Silver, Moissanite'),
    ],

    "cheshuya-bra.html": [
        ('Price: $4,000.00 MXN', 'Price: $2,000.00 MXN'),
    ],

    "cheshuya-belt.html": [
        ('data-desc="Material: 20mm Mother-of-Pearl Shells"', 'data-desc="Motherpearl Shells"'),
        ('Material: 20mm Mother-of-Pearl Shells', 'Material: Motherpearl Shells'),
    ],
}

for fname, replacements in fixes.items():
    try:
        with open(fname, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"NOT FOUND: {fname}")
        continue

    changed = False
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"  Fixed in {fname}: '{old[:60]}' -> '{new[:60]}'")
            changed = True
        else:
            print(f"  NOT FOUND in {fname}: '{old[:60]}'")

    if changed:
        with open(fname, "w") as f:
            f.write(content)

print("\nDone!")
