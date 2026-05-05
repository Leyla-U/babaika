import os
import glob
import re

def replace_in_file(filepath, replacements):
    with open(filepath, 'r') as f:
        content = f.read()
        
    original = content
    for old, new in replacements:
        content = content.replace(old, new)
        
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {filepath}")

# 1. cheshuya-necklace-2.html (10mm)
replace_in_file('cheshuya-necklace-2.html', [
    ('Material: Motherpearl Shells', 'Material: 10mm Motherpearl Shells'),
    ('data-desc="Motherpearl Shells"', 'data-desc="10mm Motherpearl Shells"'),
    ('`Material: Motherpearl Shells`', '`Material: 10mm Motherpearl Shells`')
])

# 2. cheshuya-belt.html (20mm)
# Note: In cheshuya-belt.html, it currently says "Motherpearl Shells".
replace_in_file('cheshuya-belt.html', [
    ('Material: Motherpearl Shells', 'Material: 20mm Motherpearl Shells'),
    ('data-desc="Motherpearl Shells"', 'data-desc="20mm Motherpearl Shells"'),
    ('`Material: Motherpearl Shells`', '`Material: 20mm Motherpearl Shells`')
])

# 3. cheshuya.html
# It has artifact_detail_row_10 (10mm) and artifact_detail_row_13 (20mm)
replace_in_file('cheshuya.html', [
    ('<p class="artifact-detail-row" data-i18n="artifact_detail_row_10">Material: Motherpearl Shells</p>',
     '<p class="artifact-detail-row" data-i18n="artifact_detail_row_10">Material: 10mm Motherpearl Shells</p>'),
    ("'artifact_detail_row_10': `Material: Motherpearl Shells`",
     "'artifact_detail_row_10': `Material: 10mm Motherpearl Shells`"),
     
    ('<p class="artifact-detail-row" data-i18n="artifact_detail_row_13">Material: Mother-of-Pearl Shells</p>',
     '<p class="artifact-detail-row" data-i18n="artifact_detail_row_13">Material: 20mm Motherpearl Shells</p>'),
    ("'artifact_detail_row_13': `Material: Mother-of-Pearl Shells`",
     "'artifact_detail_row_13': `Material: 20mm Motherpearl Shells`")
])

# 4. index.html, index_es.html, index_ru.html
for f in ['index.html', 'index_es.html', 'index_ru.html']:
    if os.path.exists(f):
        # The first shell is index_auto_38 (Motherpearl Shells), the second is index_auto_39 (20mm Motherpearl Shells)
        # Wait, for index_es/ru, they might have translations, let's just replace the English ones if they exist
        replace_in_file(f, [
            ('<p class="artifact-desc" data-i18n="index_auto_38">Motherpearl Shells</p>',
             '<p class="artifact-desc" data-i18n="index_auto_38">10mm Motherpearl Shells</p>'),
            ("'index_auto_38': `Motherpearl Shells`",
             "'index_auto_38': `10mm Motherpearl Shells`"),
            
            ('<p class="artifact-desc" data-i18n="index_auto_39">20mm Motherpearl Shells</p>',
             '<p class="artifact-desc" data-i18n="index_auto_39">20mm Motherpearl Shells</p>'), # Already 20mm? Let's check format
            ("'index_auto_39': `20mm Motherpearl Shells`",
             "'index_auto_39': `20mm Motherpearl Shells`")
        ])

print("Done updating shell sizes.")
