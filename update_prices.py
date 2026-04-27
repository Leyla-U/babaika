import os
import re

prices = {
    '01.01': 'price_1TQafZJPn6LmQgwJSTbUQcgy',
    '01.02': 'price_1TQb10JPn6LmQgwJFMS0HaD1',
    '01.03': 'price_1TQat4JPn6LmQgwJ9aw8fNsg',
    '01.04': 'price_1TQauVJPn6LmQgwJzUjCNjNn',
    
    '02.01': 'price_1TQawkJPn6LmQgwJxf39q6Tp',
    '02.02': 'price_1TQaznJPn6LmQgwJ32TalPuF',
    '02.04': 'price_1TQbHgJPn6LmQgwJaPMB2nHF',
    
    '03.01': 'price_1TQbKfJPn6LmQgwJbKLAxkSv', # Chiffon
    '03.02': 'price_1TQbMZJPn6LmQgwJsozGfeXn', # Cotton
    '03.03': 'price_1TQbOCJPn6LmQgwJZOP555Oj',
    '03.04': 'price_1TQbVlJPn6LmQgwJf0pX9yL7',
    
    '04.01': 'price_1TQbXMJPn6LmQgwJn3zZwNpx',
    '04.02': 'price_1TQbZ1JPn6LmQgwJE9rPJZwV',
    
    '05.01': 'price_1TQbbKJPn6LmQgwJfRKnPQqs',
    '05.02': 'price_1TQbt5JPn6LmQgwJ6kY8NMp7',
    '05.03': 'price_1TQbcaJPn6LmQgwJ8KmQBiAk',
    
    '06.01': 'price_1TQbiFJPn6LmQgwJmgpuP2KF',
    '06.02': 'price_1TQbjaJPn6LmQgwJ2OB1nFZK',
    '06.03': 'price_1TQblYJPn6LmQgwJNk7Hoful',
    '06.04': 'price_1TQbnBJPn6LmQgwJMZeGPJod',
    
    '07.01': 'price_1TQbruJPn6LmQgwJ6preZbIS',
    '07.02': 'price_1TQbuvJPn6LmQgwJOlissPz3',
    '07.03': 'price_1TQbtkJPn6LmQgwJSCBixnQx',
    '07.04': 'price_1TQbuGJPn6LmQgwJSJrzJk7Q',
}

files = [f for f in os.listdir('.') if f.endswith('.html')]

for f in files:
    with open(f, 'r') as file:
        content = file.read()
        
    original = content
    
    for _id, price_id in prices.items():
        # Match <button class="btn-add-cart ... " data-id="01.01" ... >
        # We'll just replace `data-id="01.01"` with `data-id="01.01" data-price-id="price_1TQ..."`
        # But ensure we don't duplicate it if already there
        if f'data-price-id="{price_id}"' not in content:
            content = re.sub(
                fr'data-id="{_id}"(?! data-price-id)',
                f'data-id="{_id}" data-price-id="{price_id}"',
                content
            )
            
    if content != original:
        with open(f, 'w') as file:
            file.write(content)
        print(f"Updated {f}")

