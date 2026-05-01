import glob, re

for fname in glob.glob("*.html"):
    with open(fname, "r") as f:
        content = f.read()

    original = content

    def replace_kimono(match):
        # Get surrounding context to check if it's inside an href, src, or filename
        return match.group(0)

    # We'll use a tokenizer approach: replace kimono only in text/attribute VALUES
    # but NOT in href="...", src="...", data-price-id="...", id="..." that contain filenames
    
    def smart_replace(text):
        # Replace in attribute values that are display text (not URLs/IDs)
        # Strategy: replace all, then restore URLs (hrefs, srcs)
        
        # Step 1: collect all href/src values to preserve them
        url_attrs = re.findall(r'(?:href|src|data-price-id|id)="([^"]*kimono[^"]*)"', text, re.IGNORECASE)
        
        # Step 2: do the replacements
        result = text
        result = re.sub(r'\bKIMONO\b', 'WRAP', result)
        result = re.sub(r'\bKimono\b', 'Wrap', result)
        result = re.sub(r'\bkimono\b', 'wrap', result)
        
        # Step 3: restore URLs that were incorrectly changed
        for original_url in url_attrs:
            changed_url = original_url
            changed_url = re.sub(r'\bWRAP\b', 'KIMONO', changed_url)
            changed_url = re.sub(r'\bWrap\b', 'Kimono', changed_url)
            changed_url = re.sub(r'\bwrap\b', 'kimono', changed_url)
            if changed_url != original_url:
                result = result.replace(f'"{changed_url}"', f'"{original_url}"')
        
        return result

    content = smart_replace(content)

    if content != original:
        with open(fname, "w") as f:
            f.write(content)
        print(f"Updated: {fname}")

print("Done!")
