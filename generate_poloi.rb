require 'json'

chiffon_main = [
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173937/babaika_film_03_hnyeed.jpg",
  "https://res.cloudinary.com/dejpm4v8y/video/upload/v1777172643/poloic_uyjq9u.mp4",
  "https://res.cloudinary.com/dejpm4v8y/video/upload/v1777169031/pc2_fsgmnp.mp4",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152784/pc6_xrhx6c.png",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152783/pc5_pk4mto.png",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152782/pc3_bc82ef.png",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152390/babaika_delta_09_jce7u6.jpg",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777233020/babaika_delta_42_cbz1xj.jpg",
  "https://res.cloudinary.com/dejpm4v8y/video/upload/v1777088810/poloi-video_aw19zc.mp4",
  "https://res.cloudinary.com/dejpm4v8y/video/upload/v1777081971/poloi-chiffon-fabric_pcsqfm.mp4"
]

chiffon_full = [
  "https://res.cloudinary.com/dejpm4v8y/video/upload/v1777169029/pc-video_v9hu3v.mp4",
  "https://res.cloudinary.com/dejpm4v8y/video/upload/v1777169030/pc3_vqoczp.mp4",
  "https://res.cloudinary.com/dejpm4v8y/video/upload/v1777169031/pc2_fsgmnp.mp4",
  "https://res.cloudinary.com/dejpm4v8y/video/upload/v1777169039/pc4_c3krdv.mp4",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777233021/babaika_delta_48_tevxlv.jpg",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777233018/babaika_delta_21_uwfjsc.jpg",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777233016/babaika_delta_13_fbfukt.jpg",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777233015/babaika_delta_12_xojqyd.jpg",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173940/babaika_film_08_wptgbt.jpg",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173939/babaika_film_07_f78yif.jpg",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173937/babaika_film_03_hnyeed.jpg",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152391/babaika_delta_26_pxts3a.jpg",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152390/babaika_delta_19_bfd8m6.jpg",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152391/babaika_delta_35_lxxneh.jpg",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152782/pc4_by1fvt.png",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152781/pc2_xrahtu.png",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152373/babaika_delta_31_ffsyt4.jpg"
].uniq - chiffon_main

cotton_main = [
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777233449/poloidd_bzraoq.png",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152980/pcs3_enrcde.png",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152985/psc1_s0obmr.png",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152986/psc2_f9jtty.png",
  "https://res.cloudinary.com/dejpm4v8y/video/upload/v1777172297/poloisc_arpzcm.mp4",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777153179/psc8_kggil9.png",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777153181/psc7_kmsqof.png",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777153183/psc5_ltv8dh.png",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777153183/psc6_zo5kpt.png"
]

cotton_full = [
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777153183/psc6_zo5kpt.png",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777153178/pcs4_aslocz.png",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152983/PLI_nbqzy1.jpg"
].uniq - cotton_main

bra_main = [
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173885/babaika_film_21_hrhqxa.jpg",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173885/babaika_film_25_v7rqgf.jpg",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173884/babaika_film_24_fbfgiy.jpg",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152373/babaika_delta_32_dhqz2e.jpg",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152373/babaika_delta_30_rzpquc.jpg",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152373/babaika_delta_44_yimmti.jpg",
  "https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152373/babaika_delta_31_ffsyt4.jpg",
  "https://res.cloudinary.com/dejpm4v8y/video/upload/v1777172643/poloic_uyjq9u.mp4"
]

def make_html(files, class_name='')
  files.map do |url|
    if url.end_with?('.mp4')
      "<video #{class_name != '' ? "class=\"#{class_name}\"" : ''} src=\"#{url}\" autoplay loop muted playsinline></video>"
    else
      "<img #{class_name != '' ? "class=\"#{class_name}\"" : ''} src=\"#{url}\" alt=\"\" />"
    end
  end.join("\n            ")
end

File.write('assets_generated.rb', "
@chiffon_main_html = %q{#{make_html(chiffon_main)}}
@chiffon_hidden_html = %q{#{make_html(chiffon_full, 'hidden')}}
@cotton_main_html = %q{#{make_html(cotton_main)}}
@cotton_hidden_html = %q{#{make_html(cotton_full, 'hidden')}}
@bra_main_html = %q{#{make_html(bra_main)}}
")

puts "Done"
