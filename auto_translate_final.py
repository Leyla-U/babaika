import os
import glob
import re
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='auto', target='es')

def translate_html_content(html, filepath):
    en_dict = {}
    es_dict = {}
    idx = 0
    
    # We will look for p, h1-h6, button, a, span
    # We explicitly exclude script, style, etc.
    pattern = re.compile(r'(<(p|h[1-6]|button|a|span)(?![^>]*\bdata-i18n\b)[^>]*)>([\s\S]*?)(</\2>)', re.IGNORECASE)
    
    # We also keep track of translations to avoid duplicates and save API calls
    cache = {}

    def replacer(match):
        nonlocal idx
        tag_open = match.group(1)
        tag_name = match.group(2).lower()
        content = match.group(3)
        tag_close = match.group(4)
        
        # skip if data-i18n is inside the tag_open (handled by regex lookahead, but just to be sure)
        if 'data-i18n=' in tag_open:
            return match.group(0)
            
        # skip if content has other tags (except br)
        clean_content = re.sub(r'<br\s*/?>', ' ', content, flags=re.IGNORECASE)
        if '<' in clean_content or '>' in clean_content:
            return match.group(0)
            
        text = content.strip()
        
        # skip empty
        if not text or len(text) < 2:
            return match.group(0)
            
        # skip if it's purely numbers, punctuation, or single letters
        if re.match(r'^[\d\s\.\-\/\:\[\]\(\)\+]+$', text):
            return match.group(0)
            
        # skip specific words that shouldn't be translated or are already handled
        if text.lower() in ['babaika', 'en', 'es', 'ru', 'cart', 'close', 'instagram']:
            return match.group(0)
            
        # skip if it contains a template literal like ${...} to avoid breaking js
        if '${' in text:
            return match.group(0)
            
        # check if it's mostly a path or url
        if text.startswith('http') or text.endswith('.jpg') or text.endswith('.png'):
            return match.group(0)
            
        key = f"final_auto_{tag_name}_{idx}"
        idx += 1
        
        text_for_trans = text.replace('<br>', '\n').replace('<br/>', '\n')
        
        if text_for_trans in cache:
            es_text = cache[text_for_trans]
        else:
            try:
                es_text = translator.translate(text_for_trans)
                es_text = es_text.replace('\n', '<br>')
                cache[text_for_trans] = es_text
            except:
                es_text = text
                
        en_dict[key] = text
        es_dict[key] = es_text
        
        # For 'a' tags, if they have an href that is exactly the same as the text (like an email), don't translate
        if tag_name == 'a' and ('mailto:' in tag_open or '@' in text):
            return match.group(0)
        
        return tag_open + f' data-i18n="{key}">' + content + tag_close

    html = pattern.sub(replacer, html)
    return html, en_dict, es_dict

def update_translation_block(html, new_en, new_es):
    if not new_en:
        return html
        
    # Create safe javascript strings by escaping backticks and template literals
    def escape_js(s):
        s = s.replace('`', '\\`')
        s = s.replace('${', '\\${')
        return s
        
    en_additions = ",\n        " + ",\n        ".join([f"'{k}': `{escape_js(v)}`" for k,v in new_en.items()])
    es_additions = ",\n        " + ",\n        ".join([f"'{k}': `{escape_js(v)}`" for k,v in new_es.items()])
    
    def insert_en(m):
        content = m.group(1)
        content = re.sub(r',\s*$', '', content)
        return "en: {" + content + en_additions + "\n      }"
        
    def insert_es(m):
        content = m.group(1)
        content = re.sub(r',\s*$', '', content)
        return "es: {" + content + es_additions + "\n      }"
        
    html = re.sub(r'en:\s*\{([\s\S]*?)\n\s*\}', insert_en, html, count=1)
    html = re.sub(r'es:\s*\{([\s\S]*?)\n\s*\}', insert_es, html, count=1)
    
    return html

def process_file(filepath):
    print(f"Processing {filepath}...")
    with open(filepath, 'r') as f:
        html = f.read()
        
    original = html
    new_html, en_dict, es_dict = translate_html_content(html, filepath)
    new_html = update_translation_block(new_html, en_dict, es_dict)
    
    if new_html != original:
        print(f"Updated {filepath} with {len(en_dict)} new translations")
        with open(filepath, 'w') as f:
            f.write(new_html)

for file in glob.glob("*.html"):
    if file.startswith("index_") or file.startswith("about_"):
        continue
    process_file(file)
