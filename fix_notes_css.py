import os
import glob
import re

css = """
    .cart-notes-group {
      padding: 16px 0 8px;
    }
    .cart-notes-group label {
      display: block;
      font-size: 10px;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--text);
      margin-bottom: 8px;
    }
    .cart-notes-group textarea {
      width: 100%;
      box-sizing: border-box;
      background: transparent;
      border: 1px solid var(--line);
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 100;
      color: var(--text);
      padding: 10px;
      outline: none;
      resize: vertical;
      min-height: 72px;
      line-height: 1.7;
      transition: border-color 0.2s;
      overflow-y: auto;
    }
    .cart-notes-group textarea:focus { border-color: var(--text); }
    .cart-notes-group textarea::placeholder { color: var(--text-faint); font-style: italic; font-size: 11px; }
    .cart-notes-hint {
      font-size: 12px;
      color: var(--text);
      font-style: italic;
      line-height: 1.6;
      margin-top: 6px;
    }
"""

files = glob.glob('/Users/leylaudimamedova/babaika/*.html')
exclude = {'about.html', 'about_es.html', 'about_ru.html', 'index_es.html', 'index_ru.html', 'success.html', 'shipping.html', 'catalogue.html'}

updated = 0
for filepath in files:
    filename = os.path.basename(filepath)
    if filename in exclude: continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if '.cart-notes-group {' in content:
        # Already has CSS, remove old to replace
        content = re.sub(r'\s*\.cart-notes-group \{.*?(?=</style>)', '\n' + css, content, flags=re.DOTALL)
    else:
        # Does not have CSS, inject before </style>
        content = content.replace('</style>', css + '\n</style>', 1)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    updated += 1
        
print(f"Done. Updated {updated} files.")
