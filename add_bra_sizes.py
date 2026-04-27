import re

files = ['tuman-bra.html', 'tamarisk-bra.html', 'poloi-bra.html', 'cheshuya-bra.html']

replacement_html = """<div class="artifact-detail-row" style="margin-top:12px; margin-bottom:12px; display:flex; align-items:center; gap:12px;">
  <label for="bra-size" style="margin:0;">Size:</label>
  <select id="bra-size" style="background:transparent; color:var(--text); border:1px solid var(--line); font-family:var(--font-mono); font-size:11px; padding:6px 12px; text-transform:uppercase; outline:none; cursor:pointer;">
    <option value="XS-S">XS-S</option>
    <option value="M-L">M-L</option>
  </select>
</div>
<script>
  document.addEventListener("DOMContentLoaded", () => {
    const sizeSelect = document.getElementById('bra-size');
    const addBtn = document.querySelector('.btn-add-cart');
    if (sizeSelect && addBtn) {
      const baseId = addBtn.dataset.id;
      const baseName = addBtn.dataset.name;
      sizeSelect.addEventListener('change', (e) => {
        const size = e.target.value;
        addBtn.dataset.id = baseId + '-' + size;
        addBtn.dataset.name = baseName + ' (' + size + ')';
      });
      // Initial setup
      addBtn.dataset.id = baseId + '-' + sizeSelect.value;
      addBtn.dataset.name = baseName + ' (' + sizeSelect.value + ')';
    }
  });
</script>"""

for filename in files:
    with open(filename, 'r') as f:
        content = f.read()

    # Replace the Size line
    # Depending on the file, it might have margin-top:8px or not
    pattern = re.compile(r'<p class="artifact-detail-row"[^>]*>\s*Size:\s*One size\s*</p>')
    new_content = pattern.sub(replacement_html, content)
    
    if new_content != content:
        with open(filename, 'w') as f:
            f.write(new_content)
        print(f"Updated sizes in {filename}")
    else:
        print(f"Failed to find Size line in {filename}")

