#!/usr/bin/env python3
"""Remove Russian language from all Babaika HTML pages."""

import re, os, glob

BASE = '/Users/leylaudimamedova/babaika'

pages = glob.glob(os.path.join(BASE, '*.html'))
changed = []

for path in pages:
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html

    # 1. Remove the ru: { ... } block from TRANSLATIONS (handles multi-line)
    html = re.sub(
        r",?\s*ru\s*:\s*\{[^}]*\}",
        '',
        html,
        flags=re.DOTALL
    )

    # 2. Remove RU lang switcher spans/links (header + footer variants)
    # e.g.: / <span id="lang-ru" onclick="setLang('ru')">RU</span>
    # e.g.: / <span id="footer-lang-ru" onclick="setLang('ru')">RU</span>
    html = re.sub(
        r"\s*/\s*<span[^>]*(?:lang-ru|footer-lang-ru)[^>]*>RU</span>",
        '',
        html
    )
    html = re.sub(
        r"\s*/\s*<a[^>]*(?:lang-ru|footer-lang-ru)[^>]*>RU</a>",
        '',
        html
    )

    # 3. Remove 'ru' from the active-state loop array ['en','es','ru']
    html = html.replace("'en','es','ru'", "'en','es'")
    html = html.replace('"en","es","ru"', '"en","es"')

    # 4. Remove any 'ru' from forEach prefix loops like ['lang','footer-lang']
    # (these are fine, they just won't find a ru element anymore)

    # 5. Remove footer-lang-ru and lang-ru getElementById references in applyLang
    # These will now just return null which is handled safely

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        changed.append(os.path.basename(path))
        print(f'  UPDATED: {os.path.basename(path)}')
    else:
        print(f'  unchanged: {os.path.basename(path)}')

print(f'\nDone. Changed {len(changed)} files.')
