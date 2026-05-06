import glob
import re
import json

new_earring_mat = "the ear connection: silver. the flower: tin, copper, silver, the chain: steel. the river pearls."

for filepath in glob.glob("*.html"):
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # 1. Update PRICE Maps
    # Use regex to find and modify the maps
    def update_num_map(match):
        map_str = match.group(1)
        map_dict = json.loads(map_str)
        map_dict["01.03"] = 1400.0
        map_dict["01.02"] = 2900.0
        return f"const PRICE_NUM_MAP = {json.dumps(map_dict)};"
        
    def update_disp_map(match):
        map_str = match.group(1)
        map_dict = json.loads(map_str)
        map_dict["01.03"] = "$1,400.00 MXN"
        map_dict["01.02"] = "$2,900.00 MXN"
        return f"const PRICE_DISP_MAP = {json.dumps(map_dict)};"
        
    content = re.sub(r'const PRICE_NUM_MAP = ({.*?});', update_num_map, content)
    content = re.sub(r'const PRICE_DISP_MAP = ({.*?});', update_disp_map, content)

    # 2. Update Tuman Earring button data-desc
    # data-id="01.03" data-name="Tuman — Earring" data-price-id=...
    content = re.sub(
        r'(<button[^>]*data-id="01\.03"[^>]*)data-desc="[^"]*"',
        rf'\1data-desc="{new_earring_mat}"',
        content
    )

    # 3. Update Tuman Earring page text (tuman-earring.html)
    if filepath == "tuman-earring.html":
        content = re.sub(r'Material:\s*Silver,\s*River\s*Pearls', f'Material: {new_earring_mat}', content)
        content = re.sub(r'Price:\s*\$800\.00\s*MXN', 'Price: $1,400.00 MXN', content)

    # 4. Update Tuman Ring page text (tuman-ring.html)
    if filepath == "tuman-ring.html":
        content = re.sub(r'Price:\s*\$[0-9,]+\.00\s*MXN', 'Price: $2,900.00 MXN', content)

    # 5. Update index.html and catalogue.html and tuman.html (category pages)
    # They have blocks like:
    # <a href="tuman-earring.html" class="cat-item">
    # ...
    # <span class="cat-item-desc">Silver, River Pearls</span>
    # <span class="cat-item-price">$800.00 MXN</span>
    # </a>
    # We can use targeted replacements for these specific files
    
    # For Earring description in catalogue/index
    if filepath in ["index.html", "catalogue.html", "tuman.html"]:
        # Find the block for tuman-earring.html and replace inside it
        def replace_earring_block(match):
            block = match.group(0)
            block = re.sub(r'(<span[^>]*class="(cat-item-desc|artifact-desc)"[^>]*>).*?(</span>|</p>)', rf'\1{new_earring_mat}\3', block)
            block = re.sub(r'(<span[^>]*class="cat-item-price"[^>]*>).*?(</span>)', rf'\1$1,400.00 MXN\2', block)
            return block
        
        # In index.html the link is onclick="window.location='tuman-earring.html'"
        # In catalogue/tuman it's <a href="tuman-earring.html">...</a>
        # We can just look for the general block context
        content = re.sub(r'<a href="tuman-earring\.html"[^>]*>[\s\S]*?</a>', replace_earring_block, content)
        
        # For index.html, it's a div containing the video
        content = re.sub(r'<div[^>]*onclick="window\.location=\'tuman-earring\.html\'"[^>]*>[\s\S]*?</div>', replace_earring_block, content)
        
        # Now for Tuman Ring price
        def replace_ring_block(match):
            block = match.group(0)
            block = re.sub(r'(<span[^>]*class="cat-item-price"[^>]*>).*?(</span>)', rf'\1$2,900.00 MXN\2', block)
            return block
            
        content = re.sub(r'<a href="tuman-ring\.html"[^>]*>[\s\S]*?</a>', replace_ring_block, content)
        content = re.sub(r'<div[^>]*onclick="window\.location=\'tuman-ring\.html\'"[^>]*>[\s\S]*?</div>', replace_ring_block, content)

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated in {filepath}")

