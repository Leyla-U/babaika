#!/usr/bin/env python3
"""
Fix i18n issues across all Babaika pages:
1. tuman.html: fix Next Chapter button to use next-chapter-btn class
2. All pages: add data-i18n to [ TEXTILE ARTIFACTS ] / [ HARDWARE ARTIFACTS ] labels
3. All pages: add translation keys for these labels to each page's TRANSLATIONS dict
"""

import re
import os

BASE = '/Users/leylaudimamedova/babaika'

PAGES = [
    'index.html',
    'tuman.html',
    'tamarisk.html',
    'poloi.html',
    'il.html',
    'raskaty.html',
    'kamish.html',
    'cheshuya.html',
]

# Translation additions for each language
LABEL_TRANSLATIONS = {
    'en': {
        'lbl_textile': '[ TEXTILE ARTIFACTS ]',
        'lbl_hardware': '[ HARDWARE ARTIFACTS ]',
        'lbl_classification': '[ CLASSIFICATION ]',
        'lbl_field_notes': '[ FIELD NOTES ]',
        'lbl_identity': '[ IDENTITY ]',
        'lbl_translation': '[ TRANSLATION NOTE ]',
    },
    'es': {
        'lbl_textile': '[ ARTEFACTOS TEXTILES ]',
        'lbl_hardware': '[ ARTEFACTOS DE HARDWARE ]',
        'lbl_classification': '[ CLASIFICACIÓN ]',
        'lbl_field_notes': '[ NOTAS DE CAMPO ]',
        'lbl_identity': '[ IDENTIDAD ]',
        'lbl_translation': '[ NOTA DE TRADUCCIÓN ]',
    },
    'ru': {
        'lbl_textile': '[ ТЕКСТИЛЬНЫЕ АРТЕФАКТЫ ]',
        'lbl_hardware': '[ АППАРАТНЫЕ АРТЕФАКТЫ ]',
        'lbl_classification': '[ КЛАССИФИКАЦИЯ ]',
        'lbl_field_notes': '[ ПОЛЕВЫЕ ЗАМЕТКИ ]',
        'lbl_identity': '[ ИДЕНТИФИКАЦИЯ ]',
        'lbl_translation': '[ ПРИМЕЧАНИЕ К ПЕРЕВОДУ ]',
    }
}

def add_data_i18n_to_labels(html):
    """Add data-i18n attributes to section label elements."""
    # [ TEXTILE ARTIFACTS ] labels (on index page - without number)
    html = re.sub(
        r'(<p class="artifact-section-title"[^>]*>)\s*\[ TEXTILE ARTIFACTS \]\s*</p>',
        r'<p class="artifact-section-title" data-i18n="lbl_textile">[ TEXTILE ARTIFACTS ]</p>',
        html
    )
    # [ HARDWARE ARTIFACTS ] labels (on index page)
    html = re.sub(
        r'(<p class="artifact-section-title"[^>]*>)\s*\[ HARDWARE ARTIFACTS \]\s*</p>',
        r'<p class="artifact-section-title" data-i18n="lbl_hardware">[ HARDWARE ARTIFACTS ]</p>',
        html
    )
    # [ CLASSIFICATION ] labels on chapter pages
    html = re.sub(
        r'(<(?:p|span) class="(?:chapter-label|col-sub-tag|col-tag)"[^>]*>)\s*\[ CLASSIFICATION \]\s*</(?:p|span)>',
        lambda m: m.group(0).replace('[ CLASSIFICATION ]', '').replace('>', ' data-i18n="lbl_classification">[ CLASSIFICATION ]</').replace('<//', '</'),
        html
    )
    # [ FIELD NOTES ] labels
    html = re.sub(
        r'(<(?:p|span) class="col-tag"[^>]*>)\s*\[ FIELD NOTES \]\s*</(?:p|span)>',
        r'<span class="col-tag" data-i18n="lbl_field_notes">[ FIELD NOTES ]</span>',
        html
    )
    # [ IDENTITY ] labels
    html = re.sub(
        r'(<(?:p|span) class="col-tag"[^>]*>)\s*\[ IDENTITY \]\s*</(?:p|span)>',
        r'<span class="col-tag" data-i18n="lbl_identity">[ IDENTITY ]</span>',
        html
    )
    # [ TRANSLATION NOTE ] artifact tags
    html = re.sub(
        r'(<(?:strong)[^>]*>)\s*\[ TRANSLATION NOTE \]\s*</strong>',
        r'<strong style="font-style:normal; font-weight:200; letter-spacing:0.08em;" data-i18n="lbl_translation">[ TRANSLATION NOTE ]</strong>',
        html
    )
    return html

def add_keys_to_translation_dict(html, lang, keys_dict):
    """Insert missing translation keys into the TRANSLATIONS[lang] block."""
    # Find the language block, e.g. es: { ... }
    # We'll insert after the last key in that block
    lang_pattern = re.compile(
        rf"({lang}:\s*{{[^}}]*?)(\s*}})",
        re.DOTALL
    )
    
    def insert_keys(m):
        block = m.group(1)
        closing = m.group(2)
        additions = ''
        for key, value in keys_dict.items():
            # Only add if key doesn't already exist
            if f"'{key}'" not in block and f'"{key}"' not in block:
                additions += f"\n        {key}: '{value}',"
        return block + additions + closing
    
    return lang_pattern.sub(insert_keys, html, count=1)

def fix_tuman_next_chapter_button(html):
    """Fix tuman.html's Next Chapter button to use next-chapter-btn class."""
    return html.replace(
        'class="btn-glass" data-i18n="next_chapter_tamarisk">Next Chapter // Tamarisk</button>',
        'class="btn-glass next-chapter-btn" data-name="Tamarisk">Next Chapter // Tamarisk</button>'
    )

changed_files = []

for page in PAGES:
    path = os.path.join(BASE, page)
    if not os.path.exists(path):
        print(f'  SKIP (not found): {page}')
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()
    
    html = original
    
    # Fix 1: tuman.html Next Chapter button
    if page == 'tuman.html':
        html = fix_tuman_next_chapter_button(html)
    
    # Fix 2: Add data-i18n attributes to labels
    html = add_data_i18n_to_labels(html)
    
    # Fix 3: Add translation keys to TRANSLATIONS dict
    for lang, keys in LABEL_TRANSLATIONS.items():
        html = add_keys_to_translation_dict(html, lang, keys)
    
    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        changed_files.append(page)
        print(f'  UPDATED: {page}')
    else:
        print(f'  unchanged: {page}')

print(f'\nDone. Changed {len(changed_files)} files: {changed_files}')
