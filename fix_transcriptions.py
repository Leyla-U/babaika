import os
import re

files_to_update = ['index.html']
transcriptions = {
    'ТАМАРИСК • Tamarisk': 'ТАМАРИСК • Tamarisk [ta-ma-ˈrisk]',
    'ПОЛОИ • Poloi': 'ПОЛОИ • Polói [pa-ˈlo-ee]',
    'ИЛ • Il': 'ИЛ • Il [eel]',
    'РАСКАТЫ • Raskaty': 'РАСКАТЫ • Raskáty [ras-ˈka-ti]',
    'КАМЫШ • Kamish': 'КАМЫШ • Kamish [ka-ˈmish]',
    'ЧЕШУЯ • Cheshuya': 'ЧЕШУЯ • Cheshuyá [che-shu-ˈya]'
}

for filename in files_to_update:
    with open(filename, 'r') as f:
        content = f.read()
    
    new_content = content
    for original, transcribed in transcriptions.items():
        # Only replace the one inside the chapter-label
        pattern = re.compile(rf'(<p class="chapter-label"[^>]*>){original}(</p>)')
        new_content = pattern.sub(rf'\1{transcribed}\2', new_content)

    if new_content != content:
        with open(filename, 'w') as f:
            f.write(new_content)
        print(f"Updated transcriptions in {filename}")

# Also replace the tamarisk drawing everywhere
directory = '.'
for filename in os.listdir(directory):
    if not filename.endswith('.html'):
        continue
    with open(filename, 'r') as f:
        content = f.read()
        
    old_url = 'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777141533/tamarisk_drawing_pfoo89.png'
    new_url = 'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777253509/tamarisk_drawing_pfoo89.png'
    
    if old_url in content:
        new_content = content.replace(old_url, new_url)
        with open(filename, 'w') as f:
            f.write(new_content)
        print(f"Updated tamarisk drawing in {filename}")

