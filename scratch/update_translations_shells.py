import os
import glob

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

replace_in_file('cheshuya-necklace-2.html', [
    ('`Material: Conchas de nácar`', '`Material: Conchas de nácar de 10 mm`'),
    ('`Material: Раковины перламутра`', '`Material: 10 мм Раковины перламутра`')
])

replace_in_file('cheshuya-belt.html', [
    ('`Material: Conchas de nácar`', '`Material: Conchas de nácar de 20 mm`'),
    ('`Material: Раковины перламутра`', '`Material: 20 мм Раковины перламутра`')
])

replace_in_file('cheshuya.html', [
    # ES
    ("'artifact_detail_row_10': `Material: Conchas de nácar`", "'artifact_detail_row_10': `Material: Conchas de nácar de 10 mm`"),
    ("'artifact_detail_row_13': `Material: Conchas de nácar`", "'artifact_detail_row_13': `Material: Conchas de nácar de 20 mm`"),
    # RU (if they exist)
    ("'artifact_detail_row_10': `Материал: Раковины перламутра`", "'artifact_detail_row_10': `Материал: 10 мм Раковины перламутра`"),
    ("'artifact_detail_row_13': `Материал: Раковины перламутра`", "'artifact_detail_row_13': `Материал: 20 мм Раковины перламутра`")
])
