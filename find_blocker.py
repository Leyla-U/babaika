from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('file:///Users/leylaudimamedova/babaika/index.html')
    
    # Scroll to bottom
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    
    # Wait a bit
    page.wait_for_timeout(1000)
    
    # Try to find the footer ES button
    es_btn = page.locator('#footer-lang-es')
    box = es_btn.bounding_box()
    if box:
        x = box['x'] + box['width'] / 2
        y = box['y'] + box['height'] / 2
        
        # What element is at this point?
        el = page.evaluate(f"document.elementFromPoint({x}, {y}).outerHTML")
        el_id = page.evaluate(f"document.elementFromPoint({x}, {y}).id")
        el_class = page.evaluate(f"document.elementFromPoint({x}, {y}).className")
        
        print(f"Element at footer ES button ({x}, {y}):")
        print(f"ID: {el_id}")
        print(f"Class: {el_class}")
        print(f"HTML snippet: {el[:200]}")
    else:
        print("Could not find footer-lang-es button bounding box")
        
    browser.close()
