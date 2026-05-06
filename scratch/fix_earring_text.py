import glob
import re

new_earring_mat = "the ear connection: silver. the flower: tin, copper, silver, the chain: steel. the river pearls."

for filepath in glob.glob("*.html"):
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # 1. Update data-desc for Tuman Earring button
    # The button has data-id="01.03". Replace whatever data-desc="[^"]*" is on that button.
    def replace_desc_in_button(match):
        btn = match.group(0)
        return re.sub(r'data-desc="[^"]*"', f'data-desc="{new_earring_mat}"', btn)

    content = re.sub(r'<button[^>]*data-id="01\.03"[^>]*>', replace_desc_in_button, content)

    # 2. Update Material: ... for Tuman Earring (tuman-earring.html)
    if filepath == "tuman-earring.html":
        content = re.sub(r'Material:\s*Silver,\s*Miniature\s*Pearl\s*Drops', f'Material: {new_earring_mat}', content)

    # 3. In catalogue and index, find blocks relating to tuman-earring.html and replace ALL "Silver, River Pearls" and "Silver, Miniature Pearl Drops"
    if filepath in ["index.html", "catalogue.html", "tuman.html"]:
        def replace_earring_text(match):
            block = match.group(0)
            block = block.replace("Silver, River Pearls", new_earring_mat)
            block = block.replace("Silver, Miniature Pearl Drops", new_earring_mat)
            return block
        
        content = re.sub(r'<a href="tuman-earring\.html"[^>]*>[\s\S]*?</a>', replace_earring_text, content)
        content = re.sub(r'<video[^>]*onclick="window\.location=\'tuman-earring\.html\'"[^>]*>[\s\S]*?</video>', replace_earring_text, content)
        # also match divs if they wrap it
        content = re.sub(r'<div[^>]*onclick="window\.location=\'tuman-earring\.html\'"[^>]*>[\s\S]*?</div>', replace_earring_text, content)

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed {filepath}")

