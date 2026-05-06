import glob
import re

for filepath in glob.glob("*.html"):
    with open(filepath, 'r') as f:
        content = f.read()

    original = content
    
    # Simple replacements
    content = content.replace("Silver, Moissanite", "Silver, Lab Grown Moissanite")
    content = content.replace("Silver / Rubies", "Silver / Lab Grown Rubies")
    content = content.replace("Silver / Moissanite", "Silver / Lab Grown Moissanite")
    content = content.replace("1mm Moissanite Line", "1mm Lab Grown Moissanite Line")
    content = content.replace("with rubies", "with lab grown rubies")
    content = content.replace("line of moissanites", "line of lab grown moissanites")
    
    # Just in case "synthetic" was used for stones but missed by my grep:
    content = re.sub(r'(?i)synthetic\s+rubies', 'Lab Grown Rubies', content)
    content = re.sub(r'(?i)syntetic\s+rubies', 'Lab Grown Rubies', content)
    content = re.sub(r'(?i)synthetic\s+moissanite', 'Lab Grown Moissanite', content)
    content = re.sub(r'(?i)syntetic\s+moissanite', 'Lab Grown Moissanite', content)

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated stones in {filepath}")

