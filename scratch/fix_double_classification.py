import glob

def fix():
    for filepath in glob.glob("*.html"):
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Fix spans
        bad_span = '<span class="col-sub-tag" data-i18n="lbl_classification">[ CLASSIFICATION ]</</span data-i18n="lbl_classification">[ CLASSIFICATION ]</'
        good_span = '<span class="col-sub-tag" data-i18n="lbl_classification">[ CLASSIFICATION ]</span>'
        
        # Fix paragraphs
        bad_p = '<p class="chapter-label" style="margin-bottom:20px;" data-i18n="lbl_classification">[ CLASSIFICATION ]</</p data-i18n="lbl_classification">[ CLASSIFICATION ]</'
        good_p = '<p class="chapter-label" style="margin-bottom:20px;" data-i18n="lbl_classification">[ CLASSIFICATION ]</p>'
        
        # Fix translated spans
        bad_span_es = '<span class="col-sub-tag" data-i18n="lbl_classification">[ CLASIFICACIÓN ]</</span data-i18n="lbl_classification">[ CLASIFICACIÓN ]</'
        good_span_es = '<span class="col-sub-tag" data-i18n="lbl_classification">[ CLASIFICACIÓN ]</span>'

        bad_p_es = '<p class="chapter-label" style="margin-bottom:20px;" data-i18n="lbl_classification">[ CLASIFICACIÓN ]</</p data-i18n="lbl_classification">[ CLASIFICACIÓN ]</'
        good_p_es = '<p class="chapter-label" style="margin-bottom:20px;" data-i18n="lbl_classification">[ CLASIFICACIÓN ]</p>'

        # Fix translated spans RU
        bad_span_ru = '<span class="col-sub-tag" data-i18n="lbl_classification">[ КЛАССИФИКАЦИЯ ]</</span data-i18n="lbl_classification">[ КЛАССИФИКАЦИЯ ]</'
        good_span_ru = '<span class="col-sub-tag" data-i18n="lbl_classification">[ КЛАССИФИКАЦИЯ ]</span>'

        bad_p_ru = '<p class="chapter-label" style="margin-bottom:20px;" data-i18n="lbl_classification">[ КЛАССИФИКАЦИЯ ]</</p data-i18n="lbl_classification">[ КЛАССИФИКАЦИЯ ]</'
        good_p_ru = '<p class="chapter-label" style="margin-bottom:20px;" data-i18n="lbl_classification">[ КЛАССИФИКАЦИЯ ]</p>'

        new_content = content.replace(bad_span, good_span)
        new_content = new_content.replace(bad_p, good_p)
        new_content = new_content.replace(bad_span_es, good_span_es)
        new_content = new_content.replace(bad_p_es, good_p_es)
        new_content = new_content.replace(bad_span_ru, good_span_ru)
        new_content = new_content.replace(bad_p_ru, good_p_ru)
        
        if new_content != content:
            with open(filepath, 'w') as f:
                f.write(new_content)
            print(f"Fixed {filepath}")

if __name__ == '__main__':
    fix()
