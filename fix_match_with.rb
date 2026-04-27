['poloi-kimono.html', 'poloi-bra.html'].each do |file|
  content = File.read(file)
  
  # Replace Match With links to Tuman with Poloi
  content.gsub!(/onclick="window\.location='tuman-earring\.html'"/, "onclick=\"window.location='#'\"")
  content.gsub!(/onclick="window\.location='tuman-kimono\.html'"/, "onclick=\"window.location='poloi-kimono.html'\"")
  content.gsub!(/onclick="window\.location='tuman-ring\.html'"/, "onclick=\"window.location='poloi-bra.html'\"")

  # Replace Match With titles
  content.gsub!(/>Tuman Earring<\/p>/, ">Polói Scarf</p>")
  content.gsub!(/>Tuman Kimono<\/p>/, ">Polói Kimono</p>")
  content.gsub!(/>Tuman Ring<\/p>/, ">Polói Bra</p>")

  # Replace Match With descriptions
  content.gsub!(/>Cast Silver \/ Optical Equalizer<\/p>/, ">Blue chiffon silk</p>")
  content.gsub!(/>Mulberry Silk \/ Rayon Velvet<\/p>/, ">Blue chiffon silk</p>")

  # Change the video/img paths to match Poloi
  content.gsub!(/src="images\/Tuman\/Tuman chapter\/tuman hardware\/IMG_0185\.png"/, "src=\"https://res.cloudinary.com/dejpm4v8y/image/upload/v1777173937/babaika_film_03_hnyeed.jpg\"")
  content.gsub!(/src="images\/Tuman\/Tuman chapter\/tuman kimono\/SHE00077\.png"/, "src=\"https://res.cloudinary.com/dejpm4v8y/image/upload/v1777152784/pc6_xrhx6c.png\"")
  content.gsub!(/src="https:\/\/res\.cloudinary\.com\/dejpm4v8y\/video\/upload\/v1777085507\/tuman-ring_cgwnu3\.mp4"/, "src=\"https://res.cloudinary.com/dejpm4v8y/video/upload/v1777172643/poloic_uyjq9u.mp4\"")

  File.write(file, content)
end

# Update poloi.html to point to product pages
content_poloi = File.read('poloi.html')
content_poloi.gsub!(/<div class="artifact-right" data-gallery="03_01">/, "<div class=\"artifact-right\" style=\"cursor:pointer\" onclick=\"window.location='poloi-kimono.html'\" data-gallery=\"03_01\">")
content_poloi.gsub!(/<div class="artifact-right" data-gallery="03_02">/, "<div class=\"artifact-right\" style=\"cursor:pointer\" onclick=\"window.location='poloi-kimono.html'\" data-gallery=\"03_02\">")
content_poloi.gsub!(/<div class="artifact-right" data-gallery="03_03">/, "<div class=\"artifact-right\" style=\"cursor:pointer\" onclick=\"window.location='poloi-bra.html'\" data-gallery=\"03_03\">")

File.write('poloi.html', content_poloi)

puts "Match With updated."
