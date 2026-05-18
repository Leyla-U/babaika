import os
import glob

html_files = glob.glob('/Users/leylaudimamedova/babaika/*.html')
updated_count = 0

old_block = """        const form = document.getElementById('checkout-form');
        if (form) {
            form.addEventListener('submit', () => {
                checkoutModal.classList.remove('open');
                const succ = document.getElementById('success-modal');
                if (succ) succ.classList.add('open');
            });
        }"""

new_block = """        const form = document.getElementById('checkout-form');
        if (form) {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const submitBtn = form.querySelector('button[type="submit"]');
                const originalText = submitBtn ? submitBtn.textContent : 'Send Inquiry';
                if (submitBtn) { submitBtn.textContent = 'Sending...'; submitBtn.disabled = true; }
                try {
                    const formData = new FormData(form);
                    const data = Object.fromEntries(formData.entries());
                    const res = await fetch('/api/contact', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    if (res.ok) {
                        checkoutModal.classList.remove('open');
                        const succ = document.getElementById('success-modal');
                        if (succ) succ.classList.add('open');
                        form.reset();
                    } else {
                        alert('Failed to send inquiry. Please try again.');
                    }
                } catch (err) {
                    console.error(err);
                    alert('Network error. Please try again.');
                } finally {
                    if (submitBtn) { submitBtn.textContent = originalText; submitBtn.disabled = false; }
                }
            });
        }"""

for filepath in html_files:
    with open(filepath, 'r') as f:
        content = f.read()
        
    if old_block in content:
        content = content.replace(old_block, new_block)
        with open(filepath, 'w') as f:
            f.write(content)
        updated_count += 1
        print(f"Updated {os.path.basename(filepath)}")

print(f"Total updated: {updated_count}")
