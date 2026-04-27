import re

# ── CSS to inject (once per file, inside </style> before </head>) ──────────
SIZE_CSS = """
    /* ─── SEGMENTED SIZE SELECTOR ───────────────────────────────── */
    .size-selector-row {
      display: flex;
      align-items: center;
      gap: 14px;
      margin-top: 16px;
      margin-bottom: 4px;
    }
    .size-selector-row .size-label {
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--text-faint);
      white-space: nowrap;
    }
    .size-seg {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
    }
    .size-seg button {
      background: transparent;
      border: 1px solid var(--line);
      color: var(--text-faint);
      font-family: var(--font-mono);
      font-size: 10px;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      padding: 5px 10px;
      cursor: none;
      transition: border-color 0.18s, color 0.18s, background 0.18s;
      border-radius: 2px;
    }
    .size-seg button:hover {
      border-color: var(--text);
      color: var(--text);
    }
    .size-seg button.active {
      border-color: var(--text);
      color: var(--bg);
      background: var(--text);
    }
"""

# ── Segmented selector HTML snippets ──────────────────────────────────────
BRA_SELECTOR = """\
<div class="size-selector-row">
  <span class="size-label">Size:</span>
  <div class="size-seg" id="bra-size-seg">
    <button class="active" data-size="XS-S">XS-S</button>
    <button data-size="M-L">M-L</button>
  </div>
</div>
<script>
  document.addEventListener("DOMContentLoaded", () => {
    const seg = document.getElementById('bra-size-seg');
    const addBtn = document.querySelector('.btn-add-cart');
    if (!seg || !addBtn) return;
    const baseId   = addBtn.dataset.id;
    const baseName = addBtn.dataset.name;
    let selected = 'XS-S';
    // init
    addBtn.dataset.id   = baseId + '-' + selected;
    addBtn.dataset.name = baseName + ' (' + selected + ')';
    seg.querySelectorAll('button').forEach(btn => {
      btn.addEventListener('click', () => {
        seg.querySelectorAll('button').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selected = btn.dataset.size;
        addBtn.dataset.id   = baseId + '-' + selected;
        addBtn.dataset.name = baseName + ' (' + selected + ')';
      });
    });
  });
</script>"""

RING_SELECTOR = """\
<div class="size-selector-row">
  <span class="size-label">Size:</span>
  <div class="size-seg" id="ring-size-seg">
    <button class="active" data-size="5">5</button>
    <button data-size="5½">5½</button>
    <button data-size="6">6</button>
    <button data-size="6½">6½</button>
    <button data-size="7">7</button>
    <button data-size="7½">7½</button>
    <button data-size="8">8</button>
  </div>
</div>
<script>
  document.addEventListener("DOMContentLoaded", () => {
    const seg = document.getElementById('ring-size-seg');
    const addBtn = document.querySelector('.btn-add-cart');
    if (!seg || !addBtn) return;
    const baseId   = addBtn.dataset.id;
    const baseName = addBtn.dataset.name;
    let selected = '5';
    // init
    addBtn.dataset.id   = baseId + '-' + selected;
    addBtn.dataset.name = baseName + ' (Size ' + selected + ')';
    seg.querySelectorAll('button').forEach(btn => {
      btn.addEventListener('click', () => {
        seg.querySelectorAll('button').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selected = btn.dataset.size;
        addBtn.dataset.id   = baseId + '-' + selected;
        addBtn.dataset.name = baseName + ' (Size ' + selected + ')';
      });
    });
  });
</script>"""

# Old dropdown block (what we're replacing in bra files)
OLD_BRA_DROPDOWN = re.compile(
    r'<div class="artifact-detail-row" style="[^"]*margin-top:12px[^"]*">.*?</script>',
    re.DOTALL
)

# ── Process bra files ───────────────────────────────────────────────────────
BRA_FILES = ['tuman-bra.html', 'tamarisk-bra.html', 'poloi-bra.html', 'cheshuya-bra.html']

for fname in BRA_FILES:
    with open(fname, 'r') as f:
        content = f.read()

    # Inject CSS before </style>
    if SIZE_CSS.strip() not in content:
        content = content.replace('</style>', SIZE_CSS + '\n</style>', 1)

    # Replace old dropdown block with segmented selector
    new_content = OLD_BRA_DROPDOWN.sub(BRA_SELECTOR, content)
    if new_content == content:
        print(f"WARNING: could not replace dropdown in {fname}")
    else:
        with open(fname, 'w') as f:
            f.write(new_content)
        print(f"Updated bra sizes: {fname}")

# ── Process ring files ──────────────────────────────────────────────────────
RING_FILES = ['tuman-ring.html', 'tamarisk-ring.html', 'il-ring.html', 'raskaty-ring.html']
# poloi-ring is small, check separately

# Pattern: the Size / Dimensions line in ring files
# e.g.: <p class="artifact-detail-row" style="margin-top:8px;">Size: One size</p>
#    or: <p class="artifact-detail-row" style="margin-top:8px;">Dimensions: Adjustable</p>
OLD_RING_SIZE = re.compile(
    r'<p class="artifact-detail-row"[^>]*>\s*(Size|Dimensions)[^<]*</p>'
)

for fname in RING_FILES:
    with open(fname, 'r') as f:
        content = f.read()

    # Inject CSS before </style>
    if SIZE_CSS.strip() not in content:
        content = content.replace('</style>', SIZE_CSS + '\n</style>', 1)

    # Replace old size/dimensions line with segmented selector
    new_content = OLD_RING_SIZE.sub(RING_SELECTOR, content, count=1)
    if new_content == content:
        print(f"WARNING: could not replace size line in {fname}")
    else:
        with open(fname, 'w') as f:
            f.write(new_content)
        print(f"Updated ring sizes: {fname}")

print("Done.")
