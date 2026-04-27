import re

with open('il-kimono.html', 'r') as f:
    content = f.read()

gallery_html = """<div class="thumb-strip vertical-gallery" data-thumbs="il_kimono">
          <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777182384/il111111_ft12bx.png" alt="" />
          <video src="https://res.cloudinary.com/dejpm4v8y/video/upload/v1777172873/il-8_k4sfnf.mp4" autoplay loop muted playsinline></video>
          <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777177566/SHE00384_jplxeg.png" alt="" />
          <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777177561/SHE00373_iyfe5x.png" alt="" />
          <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777177562/SHE00380_xozzjn.png" alt="" />
          <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777177559/SHE00335_yacefv.png" alt="" />
          <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173455/babaika_il_53_zjtl1v.jpg" alt="" />
          <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173415/babaika_il_08_edvwxf.jpg" alt="" />
          <img src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173414/babaika_il_05_rsiwpg.jpg" alt="" />
          
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777177560/SHE00346_zka8xo.png" alt="" />
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777177564/SHE00392_c7wpol.png" alt="" />
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777182376/il111_twxmxj.png" alt="" />
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173452/babaika_il_41_nynut6.jpg" alt="" />
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173453/babaika_il_46_p2fpoh.jpg" alt="" />
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173454/babaika_il_49_u1xwcs.jpg" alt="" />
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173419/babaika_il_28_ysz5n8.jpg" alt="" />
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173418/babaika_il_27_ixunfj.jpg" alt="" />
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173417/babaika_il_22_le3hkb.jpg" alt="" />
          <img class="hidden" src="https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173416/babaika_il_13_b2a2bi.jpg" alt="" />
          <video class="hidden" src="https://res.cloudinary.com/dejpm4v8y/video/upload/v1777172866/il-4_e2xwiw.mp4" autoplay loop muted playsinline></video>
          <video class="hidden" src="https://res.cloudinary.com/dejpm4v8y/video/upload/v1777172869/il-5_lxfhva.mp4" autoplay loop muted playsinline></video>
        </div>"""

content = re.sub(
    r'<div class="thumb-strip vertical-gallery" data-thumbs="il_kimono">.*?</div>',
    gallery_html,
    content,
    flags=re.DOTALL
)

with open('il-kimono.html', 'w') as f:
    f.write(content)
