import glob

for filepath in glob.glob("*.html"):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # We are looking for textDetails += ... \n ';
    # It looks like:
    # textDetails += item.qty + 'x ' + item.name + ' | ' + item.desc + '
    # ';
    
    if "textDetails += item.qty + 'x ' + item.name + ' | ' + item.desc + '\n';" in content:
        content = content.replace(
            "textDetails += item.qty + 'x ' + item.name + ' | ' + item.desc + '\n';",
            "textDetails += item.qty + 'x ' + item.name + ' | ' + item.desc + '\\n';"
        )
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed {filepath}")
