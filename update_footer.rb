require 'fileutils'

chapters = {
  'tuman.html' => ['tamarisk.html', 'Tamarisk'],
  'tamarisk.html' => ['poloi.html', 'Poloi'],
  'poloi.html' => ['il.html', 'Il'],
  'il.html' => ['raskaty.html', 'Raskaty'],
  'raskaty.html' => ['kamysh.html', 'Kamysh'],
  'kamysh.html' => ['cheshuya.html', 'Cheshuya']
}

footer_nav_new = <<-HTML
    <div style="display: flex; gap: 80px; flex-wrap: wrap;">
      <nav class="footer-nav" style="flex-direction: column; align-items: flex-start; gap: 12px;">
        <a href="about.html">About</a>
        <a href="catalogue.html">Catalogue</a>
        <a href="https://www.instagram.com/babaika.babaika.babaika/" target="_blank" rel="noopener noreferrer">Instagram</a>
      </nav>
      <nav class="footer-nav" style="flex-direction: column; align-items: flex-start; gap: 12px;">
        <a href="index.html">Index (Main Page)</a>
        <a href="tuman.html">01 // Tuman</a>
        <a href="tamarisk.html">02 // Tamarisk</a>
        <a href="poloi.html">03 // Poloi</a>
        <a href="il.html">04 // Il</a>
        <a href="raskaty.html">05 // Raskaty</a>
        <a href="kamysh.html">06 // Kamysh</a>
        <a href="cheshuya.html">07 // Cheshuya</a>
      </nav>
    </div>
HTML

Dir.glob('*.html').each do |file|
  content = File.read(file)
  
  # Replace footer nav
  # Pattern to match:
  # <nav class="footer-nav">
  #   <a ...>About</a>
  #   ...
  #   <a ...>Instagram</a>
  # </nav>
  
  # Be careful to match across newlines
  if content =~ /<nav class="footer-nav">.*?<\/nav>/m
    content.sub!(/<nav class="footer-nav">.*?<\/nav>/m, footer_nav_new.strip)
  end
  
  # For chapters, add next chapter button before footer
  if chapters.key?(file)
    next_url, next_name = chapters[file]
    
    button_html = <<-HTML
  <div style="display: flex; justify-content: center; padding: 120px 24px 60px;">
    <button onclick="window.location='#{next_url}'" class="btn-glass">Next Chapter // #{next_name}</button>
  </div>
HTML

    # Insert right before <!-- FOOTER --> or <footer>
    if content.include?('<!-- FOOTER -->')
      # check if it already has the button to avoid duplication
      unless content.include?("Next Chapter //")
        content.sub!('<!-- FOOTER -->', button_html + "\n  <!-- FOOTER -->")
      end
    elsif content.include?('<footer>')
      unless content.include?("Next Chapter //")
        content.sub!('<footer>', button_html + "\n  <footer>")
      end
    end
  end
  
  File.write(file, content)
end
puts "Done updating footers and next chapter buttons."
