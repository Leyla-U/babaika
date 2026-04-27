import os

template_file = 'poloi-kimono.html'
with open(template_file, 'r') as f:
    template = f.read()

def create_page(filename, artifact_id, price_id, name, material, description, note, gallery_id, visible_assets, hidden_assets):
    content = template
    
    # Basic replacements
    content = content.replace('03.01', artifact_id)
    content = content.replace('price_1TQbKfJPn6LmQgwJbKLAxkSv', price_id)
    content = content.replace('Polói Kimono', name)
    content = content.replace('Sand-washed silk chiffon', material)
    content = content.replace('The Flooded Plain.', description)
    content = content.replace('The use of sand-washed silk chiffon creates a matte, aquatic texture that mimics the surface of the delta during the flood season. The fabric’s transparency reflects the shallow, clear waters of the polói.', note)
    
    # Replace the gallery
    gallery_html = f'<div class="thumb-strip vertical-gallery" data-thumbs="{gallery_id}">'
    for asset in visible_assets:
        if asset.endswith('.mp4'):
            gallery_html += f'\n          <video src="{asset}" autoplay loop muted playsinline></video>'
        else:
            gallery_html += f'\n          <img src="{asset}" alt="" />'
    
    for asset in hidden_assets:
        if asset.endswith('.mp4'):
            gallery_html += f'\n          <video class="hidden" src="{asset}" autoplay loop muted playsinline></video>'
        else:
            gallery_html += f'\n          <img class="hidden" src="{asset}" alt="" />'
    gallery_html += '\n        </div>'
    
    import re
    content = re.sub(r'<div class="thumb-strip vertical-gallery".*?</div>', gallery_html, content, flags=re.DOTALL)
    content = content.replace('poloi_kimono_chiffon', gallery_id)
    
    # Match With section (simplifying to Chapter 06 items)
    # I'll manually fix this later or just let it be.
    
    # Explore Chapter title
    content = content.replace('Chapter 03', 'Chapter 06')
    content = content.replace('Polói', 'Kamish')
    content = content.replace('poloi.html', 'kamish.html')
    
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Created {filename}")

# 06.01 Beige Kimono
create_page(
    'kamish-kimono-beige.html',
    '06.01',
    'price_1TQbiFJPn6LmQgwJmgpuP2KF',
    'Kamish Kimono (Beige)',
    'Sand-washed satin silk',
    'The Reed Beds.',
    'The sand-washed finish provides a matte, organic texture similar to the reed stem. The beige represents the sun-dried fiber of the delta.',
    'kamish_kimono_beige',
    [
        'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777182352/kam11111_dfsfti.png',
        'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777182833/SHE00023_etr9np.png',
        'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777182832/babaika_delta_07_og8w3g.png',
        'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777182713/SHE09988_wxon8q.png'
    ],
    [
        'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777182833/SHE00010_gtuq25.png',
        'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777184252/kam3242_posi0w.png',
        'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777184260/kam131_hwtlfo.png'
    ]
)

# 06.02 Green Kimono
create_page(
    'kamish-kimono-green.html',
    '06.02',
    'price_1TQbjaJPn6LmQgwJ2OB1nFZK',
    'Kamish Kimono (Grey-Green)',
    'Sand-washed satin silk',
    'The Passage Tightens.',
    'The sand-washed finish provides a matte, organic texture similar to the reed stem. The muted grey-green represents the dense layers of new growth.',
    'kamish_kimono_green',
    [
        'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777182354/kam11111111_x4jeyl.png',
        'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777257807/kam33_d0afjo.png',
        'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777184253/kam333_kw6dgz.png',
        'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777257781/kam33333_ukrvep.png'
    ],
    [
        'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777257859/kam333333_b3oulb.png',
        'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777257793/kam3333_ezmk9f.png',
        'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777276582/kam2_jxxyab.png',
        'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777276611/kamere_ba9jm2.png',
        'https://res.cloudinary.com/dejpm4v8y/video/upload/v1777175218/kamish1_vrnrqx.mp4'
    ]
)

# 06.03 Bag
create_page(
    'kamish-bag.html',
    '06.03',
    'price_1TQblYJPn6LmQgwJNk7Hoful',
    'Kamish Bag',
    'Silk dupioni',
    'Structured Fibers.',
    'While visually mimicking dry grass, the primary purpose of the dupioni is its sound. The heavy, irregular weave creates a rustling effect reminiscent of wind moving through the reed beds.',
    'kamish_bag',
    [
        'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777184256/kambag_vyraac.png',
        'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777276561/kam_ff0zqj.png',
        'https://res.cloudinary.com/dejpm4v8y/image/upload/v1777182441/babaika_il_18_eutgbo.png'
    ],
    [
        'https://res.cloudinary.com/dejpm4v8y/video/upload/v1777085761/Tamarisk-video-1_qfx1ck.mp4'
    ]
)
