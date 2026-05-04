import os
import glob
import re

for filepath in glob.glob("*.html"):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # 1. Add data-i18n to "← Back to Archive"
    content = re.sub(r'(<a[^>]*href="[^"]*"[^>]*)>\s*← Back to Archive\s*</a>', 
                     lambda m: m.group(1) + ' data-i18n="nav_back">← Back to Archive</a>' if 'data-i18n' not in m.group(1) else m.group(0), 
                     content)

    # 2. Add data-i18n to "View" buttons
    content = re.sub(r'(<button[^>]*class="btn-glass"[^>]*)>\s*View\s*</button>', 
                     lambda m: m.group(1) + ' data-i18n="btn_view">View</button>' if 'data-i18n' not in m.group(1) else m.group(0), 
                     content)

    # 3. Add Next Chapter translation logic
    # Find next chapter buttons
    def replace_next_chapter(m):
        btn_start = m.group(1)
        chapter_name = m.group(2)
        if 'data-name' in btn_start:
            return m.group(0)
        return btn_start + f' class="btn-glass next-chapter-btn" data-name="{chapter_name}">Next Chapter // {chapter_name}</button>'
    
    content = re.sub(r'(<button[^>]*onclick="window\.location=\'[^\']+\'"[^>]*)class="btn-glass">\s*Next Chapter // ([A-Za-z]+)\s*</button>', 
                     replace_next_chapter, content)

    # Now we need to update the script block to include the generic next_chapter and replace TRANSLATIONS
    script_start = "<!-- ── TRANSLATION SYSTEM ── -->"
    if script_start in content:
        # We will replace the whole translation script to have a unified one
        unified_script = """<!-- ── TRANSLATION SYSTEM ── -->
  <script>
  (function() {
    const TRANSLATIONS = {
      en: {
        nav_back:               '← Back to Archive',
        btn_view:               'View',
        next_chapter:           'Next Chapter //',
        footer_brand:           'A Wearable Landscape Archive.<br><br>The Volga Delta, mapped through texture, memory, and myth.'
      },
      es: {
        nav_back:               '← Volver al Archivo',
        btn_view:               'Ver',
        next_chapter:           'Siguiente Capítulo //',
        footer_brand:           'Un Archivo de Paisajes Vestibles.<br><br>El Delta del Volga, cartografiado a través de la textura, la memoria y el mito.'
      },
      ru: {
        nav_back:               '← Назад к Архиву',
        btn_view:               'Посмотреть',
        next_chapter:           'Следующая Глава //',
        footer_brand:           'Архив носимых ландшафтов.<br><br>Волжская дельта — в ткани, памяти и мифе.'
      }
    };

    var lang = localStorage.getItem('babaika_lang') || 'en';

    function applyLang(l) {
      if (!TRANSLATIONS[l]) l = 'en';
      lang = l;
      localStorage.setItem('babaika_lang', l);
      document.documentElement.lang = l;

      var t = TRANSLATIONS[l];
      document.querySelectorAll('[data-i18n]').forEach(function(el) {
        var key = el.getAttribute('data-i18n');
        if (t[key] !== undefined) el.innerHTML = t[key];
      });

      document.querySelectorAll('.next-chapter-btn').forEach(function(btn) {
        var name = btn.getAttribute('data-name') || '';
        btn.innerHTML = t.next_chapter + ' ' + name;
      });

      ['en','es','ru'].forEach(function(code) {
        ['footer-lang-', 'lang-'].forEach(function(prefix) {
          var el = document.getElementById(prefix + code);
          if (!el) return;
          if (code === l) {
            el.classList.add('active');
            el.style.textDecoration = 'underline';
            el.style.textUnderlineOffset = '4px';
          } else {
            el.classList.remove('active');
            el.style.textDecoration = 'none';
          }
        });
      });
    }

    window.setLang = function(l) { applyLang(l); };
    applyLang(lang);
  })();
  </script>"""
        
        # Replace the existing translation block until the end of the script tag
        content = re.sub(r'<!-- ── TRANSLATION SYSTEM ── -->[\s\S]*?</script>', unified_script, content)
        
    if content != original:
        print(f"Fixed {filepath}")
        with open(filepath, 'w') as f:
            f.write(content)

