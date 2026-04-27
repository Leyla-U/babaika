import os
import re
from pathlib import Path

def check_images():
    workspace = "/Users/leylaudimamedova/babaika"
    html_files = list(Path(workspace).rglob("*.html"))
    
    broken_links = []
    
    # Regex to find src, href, and url() references
    pattern = re.compile(r'(?:src|href|url\()[\'"]?((?!http|https|data:|#|mailto:|tel:)[^\'"\)]+)[\'"]?\)?', re.IGNORECASE)
    
    for html_file in html_files:
        if "node_modules" in str(html_file):
            continue
            
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            matches = pattern.findall(content)
            
            for match in matches:
                # Clean path (remove query params if any)
                clean_path = match.split('?')[0].split('#')[0].strip()
                
                if not clean_path or clean_path.startswith('/'):
                    # Some paths might be root-relative, but in this project they seem to be relative to root
                    if clean_path.startswith('/'):
                        clean_path = clean_path[1:]
                
                # Check if it's a file on disk
                file_dir = html_file.parent
                path_relative_to_file = file_dir / clean_path
                path_relative_to_root = Path(workspace) / clean_path
                
                if not path_relative_to_file.exists() and not path_relative_to_root.exists():
                    # Ignore .html files and fonts (might be in fonts/ but let's see)
                    if clean_path.endswith(".html"):
                        continue
                    
                    # Ignore directory names if they exist (sometimes used in href)
                    if (Path(workspace) / clean_path).is_dir():
                        continue
                        
                    broken_links.append({
                        "file": str(html_file),
                        "link": match,
                        "path": clean_path
                    })
    
    return broken_links

if __name__ == "__main__":
    links = check_images()
    # Deduplicate
    unique_links = []
    seen = set()
    for l in links:
        key = (l['file'], l['path'])
        if key not in seen:
            unique_links.append(l)
            seen.add(key)
            
    for link in unique_links:
        print(f"File: {link['file']}\nBroken Link: {link['link']}\n")
