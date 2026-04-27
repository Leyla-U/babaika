require_relative 'assets_generated.rb'

# 1. POLOI KIMONO
content = File.read('poloi-kimono.html')

content.gsub!('<title>Babaika — Chapter 01: Tuman</title>', '<title>Babaika — Polói Kimono</title>')

# The artifact grid starts at `<div class="artifact-grid product-page-grid"`
# We will replace everything from `<div class="artifact-grid product-page-grid"` to the end of its block.
# Since it's tricky to parse HTML, we can replace a known chunk.
start_str = '<div class="artifact-grid product-page-grid" style="align-items: start;">'
end_str = '<!-- MATCH WITH IT SECTION -->'

chiffon_view = <<-HTML
  <div id="mat-chiffon" class="mat-view active artifact-grid product-page-grid" style="align-items: start;">
    <!-- LEFT COL: Info -->
    <div class="artifact-left sticky-col">
      <div class="sticky-content" style="top: 20vh; transform: none;">
        <p class="artifact-tag" style="margin-bottom: 12px;">[ TEXTILE ARTIFACT 03.01 ]</p>
        <h1 class="artifact-name" style="font-size: 32px; margin-bottom: 16px;">POLÓI KIMONO</h1>
        
        <div class="material-switch" style="display: flex; gap: 16px; margin-bottom: 24px;">
          <span class="mat-option active" data-mat="chiffon" onclick="switchMaterial('chiffon')">[ SILK CHIFFON ]</span>
          <span class="mat-option" data-mat="cotton" onclick="switchMaterial('cotton')">[ SILK / COTTON ]</span>
        </div>

        <p class="artifact-detail-row">Material: Blue chiffon silk</p>
        <p class="artifact-detail-row" style="margin-top:8px;">Size: One size</p>
        
        <div class="artifact-actions" style="margin-top: 32px; display: flex; gap: 8px; max-width: 320px;">
          <button class="btn-add-cart" data-id="03.01" data-name="Polói — Kimono" data-desc="Blue chiffon silk" style="flex:1; padding:16px; background:transparent; border:1px solid var(--line); color:var(--text); cursor:pointer; font-size:11px;">+ ADD</button>
          <button class="btn-buy-now" data-id="03.01" data-name="Polói — Kimono" data-desc="Blue chiffon silk" style="flex:1; padding:16px; background:var(--text-faint); border:1px solid var(--text-faint); color:#fff; cursor:pointer; font-size:11px;">INQUIRE</button>
        </div>

        <div style="margin-top: 48px;">
          <p class="artifact-note" style="margin-top: 0; padding-top: 0;">
            <strong style="font-style:normal; font-weight:200; letter-spacing:0.08em;">[ TRANSLATION NOTE ]</strong><br><br>
            Selected for its weightless transparency. When worn, the blue chiffon functions exactly as the polói water does—as a thin, fluid layer that covers the body in the color of the reflected sky.
          </p>
        </div>
      </div>
    </div>

    <!-- RIGHT COL: Gallery -->
    <div class="artifact-center" style="grid-column: span 2;">
      <div class="gallery-block" data-gallery="poloi_kimono_chiffon">
        <div class="photo-viewer" style="display: none;">
          <img class="main-photo" alt="Poloi Kimono Chiffon" />
          <video class="main-video" src="" autoplay loop muted playsinline></video>
          <button class="photo-nav prev">&#8592;</button>
          <button class="photo-nav next">&#8594;</button>
          <div class="photo-dots"></div>
        </div>
        
        <div class="thumb-strip vertical-gallery" data-thumbs="poloi_kimono_chiffon">
          #{@chiffon_main_html}
          #{@chiffon_hidden_html}
        </div>
        <button class="btn-full-album" onclick="openGrid('poloi_kimono_chiffon')" style="margin-top: 32px; width: 100%; padding: 16px; background: transparent; border: 1px solid var(--text); color: var(--text); font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.15em; text-transform: uppercase; cursor: none; transition: background 0.3s, color 0.3s;" onmouseover="this.style.background='var(--text)'; this.style.color='var(--bg)'" onmouseout="this.style.background='transparent'; this.style.color='var(--text)'">VIEW FULL GRID</button>
      </div>
    </div>
  </div>
HTML

cotton_view = <<-HTML
  <div id="mat-cotton" class="mat-view artifact-grid product-page-grid" style="align-items: start; display: none;">
    <!-- LEFT COL: Info -->
    <div class="artifact-left sticky-col">
      <div class="sticky-content" style="top: 20vh; transform: none;">
        <p class="artifact-tag" style="margin-bottom: 12px;">[ TEXTILE ARTIFACT 03.02 ]</p>
        <h1 class="artifact-name" style="font-size: 32px; margin-bottom: 16px;">POLÓI KIMONO</h1>
        
        <div class="material-switch" style="display: flex; gap: 16px; margin-bottom: 24px;">
          <span class="mat-option" data-mat="chiffon" onclick="switchMaterial('chiffon')">[ SILK CHIFFON ]</span>
          <span class="mat-option active" data-mat="cotton" onclick="switchMaterial('cotton')">[ SILK / COTTON ]</span>
        </div>

        <p class="artifact-detail-row">Material: Silk cotton poplin</p>
        <p class="artifact-detail-row" style="margin-top:8px;">Size: One size</p>
        
        <div class="artifact-actions" style="margin-top: 32px; display: flex; gap: 8px; max-width: 320px;">
          <button class="btn-add-cart" data-id="03.02" data-name="Polói — Kimono" data-desc="Silk cotton poplin" style="flex:1; padding:16px; background:transparent; border:1px solid var(--line); color:var(--text); cursor:pointer; font-size:11px;">+ ADD</button>
          <button class="btn-buy-now" data-id="03.02" data-name="Polói — Kimono" data-desc="Silk cotton poplin" style="flex:1; padding:16px; background:var(--text-faint); border:1px solid var(--text-faint); color:#fff; cursor:pointer; font-size:11px;">INQUIRE</button>
        </div>

        <div style="margin-top: 48px;">
          <p class="artifact-note" style="margin-top: 0; padding-top: 0;">
            <strong style="font-style:normal; font-weight:200; letter-spacing:0.08em;">[ TRANSLATION NOTE ]</strong><br><br>
            This fabric was chosen for its optical instability. It shifts color between golden brown (the silted riverbed) and blue (the sky). It captures the dual nature of the shallow water—the tension between what lies beneath and what is reflected on top.
          </p>
        </div>
      </div>
    </div>

    <!-- RIGHT COL: Gallery -->
    <div class="artifact-center" style="grid-column: span 2;">
      <div class="gallery-block" data-gallery="poloi_kimono_cotton">
        <div class="photo-viewer" style="display: none;">
          <img class="main-photo" alt="Poloi Kimono Cotton" />
          <video class="main-video" src="" autoplay loop muted playsinline></video>
          <button class="photo-nav prev">&#8592;</button>
          <button class="photo-nav next">&#8594;</button>
          <div class="photo-dots"></div>
        </div>
        
        <div class="thumb-strip vertical-gallery" data-thumbs="poloi_kimono_cotton">
          #{@cotton_main_html}
          #{@cotton_hidden_html}
        </div>
        <button class="btn-full-album" onclick="openGrid('poloi_kimono_cotton')" style="margin-top: 32px; width: 100%; padding: 16px; background: transparent; border: 1px solid var(--text); color: var(--text); font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.15em; text-transform: uppercase; cursor: none; transition: background 0.3s, color 0.3s;" onmouseover="this.style.background='var(--text)'; this.style.color='var(--bg)'" onmouseout="this.style.background='transparent'; this.style.color='var(--text)'">VIEW FULL GRID</button>
      </div>
    </div>
  </div>
HTML

# Extract the parts
pre_html = content[0...content.index(start_str)]
post_html = content[content.index(end_str)..-1]

# Rebuild poloi-kimono
final_html = pre_html + chiffon_view + cotton_view + "\n  " + post_html

# Add the script logic for switchMaterial and styles
style_to_add = "
    .mat-option { font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.2em; color: var(--text-faint); cursor: none; transition: color 0.3s; }
    .mat-option:hover { color: var(--text-muted); }
    .mat-option.active { color: var(--text); border-bottom: 1px solid var(--text); padding-bottom: 2px; }
"
final_html.gsub!('</style>', style_to_add + "\n  </style>")

script_to_add = "
    function switchMaterial(mat) {
      document.querySelectorAll('.mat-view').forEach(el => el.style.display = 'none');
      document.getElementById('mat-' + mat).style.display = 'grid';
      
      document.querySelectorAll('.mat-option').forEach(el => el.classList.remove('active'));
      document.querySelectorAll(`.mat-option[data-mat=\"${mat}\"]`).forEach(el => el.classList.add('active'));

      // If mobile, they are flex column not grid
      if (window.innerWidth <= 768) {
        document.getElementById('mat-' + mat).style.display = 'flex';
      }
      
      // Update gallery logic
      document.querySelectorAll(`#mat-${mat} .vertical-gallery`).forEach(el => {
        el.querySelectorAll('video').forEach(v => {
          v.play().catch(e=>console.log(e));
        });
      });
    }
"
final_html.gsub!('// ── Magnifying glass cursor', script_to_add + "\n    // ── Magnifying glass cursor")

# Replace "EXPLORE CHAPTER 01" with "EXPLORE CHAPTER 03"
final_html.gsub!('[ EXPLORE CHAPTER 01 ]', '[ EXPLORE CHAPTER 03 ]')
final_html.gsub!('<a href="tuman.html"', '<a href="poloi.html"')

File.write('poloi-kimono.html', final_html)

# 2. POLOI BRA
content_bra = File.read('poloi-bra.html')
content_bra.gsub!('<title>Babaika — Chapter 01: Tuman</title>', '<title>Babaika — Polói Bra</title>')

bra_html = <<-HTML
  <div class="artifact-grid product-page-grid" style="align-items: start;">
    <!-- LEFT COL: Info -->
    <div class="artifact-left sticky-col">
      <div class="sticky-content" style="top: 20vh; transform: none;">
        <p class="artifact-tag" style="margin-bottom: 12px;">[ TEXTILE ARTIFACT 03.03 ]</p>
        <h1 class="artifact-name" style="font-size: 32px; margin-bottom: 16px;">POLÓI BRA</h1>
        
        <p class="artifact-detail-row">Material: Blue chiffon silk</p>
        <p class="artifact-detail-row" style="margin-top:8px;">Size: One size</p>
        
        <div class="artifact-actions" style="margin-top: 32px; display: flex; gap: 8px; max-width: 320px;">
          <button class="btn-add-cart" data-id="03.03" data-name="Polói — Bra" data-desc="Blue chiffon silk" style="flex:1; padding:16px; background:transparent; border:1px solid var(--line); color:var(--text); cursor:pointer; font-size:11px;">+ ADD</button>
          <button class="btn-buy-now" data-id="03.03" data-name="Polói — Bra" data-desc="Blue chiffon silk" style="flex:1; padding:16px; background:var(--text-faint); border:1px solid var(--text-faint); color:#fff; cursor:pointer; font-size:11px;">INQUIRE</button>
        </div>

        <div style="margin-top: 48px;">
          <p class="artifact-note" style="margin-top: 0; padding-top: 0;">
            <strong style="font-style:normal; font-weight:200; letter-spacing:0.08em;">[ TRANSLATION NOTE ]</strong><br><br>
            Selected for its weightless transparency. When worn, the blue chiffon functions exactly as the polói water does—as a thin, fluid layer that covers the body in the color of the reflected sky.
          </p>
        </div>
      </div>
    </div>

    <!-- RIGHT COL: Gallery -->
    <div class="artifact-center" style="grid-column: span 2;">
      <div class="gallery-block" data-gallery="poloi_bra">
        <div class="photo-viewer" style="display: none;">
          <img class="main-photo" alt="Poloi Bra" />
          <video class="main-video" src="" autoplay loop muted playsinline></video>
          <button class="photo-nav prev">&#8592;</button>
          <button class="photo-nav next">&#8594;</button>
          <div class="photo-dots"></div>
        </div>
        
        <div class="thumb-strip vertical-gallery" data-thumbs="poloi_bra">
          #{@bra_main_html}
        </div>
        <button class="btn-full-album" onclick="openGrid('poloi_bra')" style="margin-top: 32px; width: 100%; padding: 16px; background: transparent; border: 1px solid var(--text); color: var(--text); font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.15em; text-transform: uppercase; cursor: none; transition: background 0.3s, color 0.3s;" onmouseover="this.style.background='var(--text)'; this.style.color='var(--bg)'" onmouseout="this.style.background='transparent'; this.style.color='var(--text)'">VIEW FULL GRID</button>
      </div>
    </div>
  </div>
HTML

pre_html_bra = content_bra[0...content_bra.index(start_str)]
post_html_bra = content_bra[content_bra.index(end_str)..-1]

final_html_bra = pre_html_bra + bra_html + "\n  " + post_html_bra
final_html_bra.gsub!('[ EXPLORE CHAPTER 01 ]', '[ EXPLORE CHAPTER 03 ]')
final_html_bra.gsub!('<a href="tuman.html"', '<a href="poloi.html"')

File.write('poloi-bra.html', final_html_bra)

puts "Pages built successfully."
