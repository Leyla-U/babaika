import os
import glob
import re

def fallback_checkout(filepath):
    with open(filepath, 'r') as f:
        html = f.read()
        
    original = html
    
    # We want to replace the try-catch block inside redirectToStripe:
    # try {
    #   const res = await fetch('/api/checkout', {
    #     ...
    #   });
    #   const data = await res.json();
    #   if (data.url) { window.location.href = data.url; }
    #   else { alert(...); checkoutBtn.textContent='Checkout'; checkoutBtn.disabled=false; }
    # } catch (err) {
    #   alert('Network error...'); checkoutBtn.textContent='Checkout'; checkoutBtn.disabled=false;
    # }
    
    new_try_catch = """      try {
        const res = await fetch('/api/checkout', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ items }),
        });

        const data = await res.json();

        if (data.url) {
          window.location.href = data.url;
        } else {
          console.error('Checkout error:', data.error);
          fallbackToModal();
        }
      } catch (err) {
        console.error('Network error:', err);
        fallbackToModal();
      }
      
      function fallbackToModal() {
        checkoutBtn.textContent = 'Checkout';
        checkoutBtn.disabled = false;
        const modal = document.getElementById('checkout-modal');
        if (modal) {
           modal.classList.add('open');
           // populate order summary for formspree
           const sumEl = document.getElementById('checkout-order-summary');
           const hiddenInput = document.getElementById('hidden-order-details');
           if (sumEl) {
               sumEl.innerHTML = '';
               let textDetails = '';
               cart.forEach(item => {
                   const p = document.createElement('p');
                   p.textContent = item.qty + 'x ' + item.name;
                   sumEl.appendChild(p);
                   textDetails += item.qty + 'x ' + item.name + ' | ' + item.desc + '\\n';
               });
               if (hiddenInput) hiddenInput.value = textDetails;
           }
        } else {
           alert('Checkout error. Please contact us directly.');
        }
      }"""
      
    # Use regex to replace the entire try-catch block
    # It starts with "try {" and ends with "} catch (err) { ... }" inside redirectToStripe
    
    pattern = r'try\s*\{\s*const res = await fetch\(\'/api/checkout\'[\s\S]*?catch\s*\(err\)\s*\{[\s\S]*?checkoutBtn\.disabled = false;\s*\}'
    
    html = re.sub(pattern, new_try_catch, html)
    
    # Let's also ensure close modal works if it was removed
    # Find if document.getElementById('checkout-modal-close').addEventListener exists
    if 'checkout-modal-close' in html and 'checkout-modal-close\').addEventListener' not in html:
        # insert before // ── Prevent cart from triggering magnifier clone issues ───
        close_logic = """
    // ── Checkout Modal Logic ──────────────────────────────────
    const checkoutModal = document.getElementById('checkout-modal');
    const checkoutModalClose = document.getElementById('checkout-modal-close');
    const checkoutModalBg = document.getElementById('checkout-modal-bg');
    if (checkoutModal) {
        if (checkoutModalClose) checkoutModalClose.addEventListener('click', () => checkoutModal.classList.remove('open'));
        if (checkoutModalBg) checkoutModalBg.addEventListener('click', () => checkoutModal.classList.remove('open'));
        
        const form = document.getElementById('checkout-form');
        if (form) {
            form.addEventListener('submit', () => {
                checkoutModal.classList.remove('open');
                const succ = document.getElementById('success-modal');
                if (succ) succ.classList.add('open');
            });
        }
    }
    const successClose = document.getElementById('success-close');
    if (successClose) {
        successClose.addEventListener('click', () => {
            const succ = document.getElementById('success-modal');
            if (succ) succ.classList.remove('open');
            cart = []; save(); renderCart(); bumpCount();
        });
    }
"""
        html = html.replace('// ── Prevent cart from triggering magnifier clone issues ───', close_logic + '\n    // ── Prevent cart from triggering magnifier clone issues ───')
        
    
    if html != original:
        with open(filepath, 'w') as f:
            f.write(html)
        print(f"Added fallback to {filepath}")

for f in glob.glob("*.html"):
    if not f.startswith("index_") and not f.startswith("about_"):
        fallback_checkout(f)
