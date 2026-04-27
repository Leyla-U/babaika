with open('il-kimono.html', 'r') as f:
    c = f.read()
c = c.replace('alt="Poloi Kimono Chiffon"', 'alt="Il Kimono"')
with open('il-kimono.html', 'w') as f:
    f.write(c)

with open('il-ring.html', 'r') as f:
    c = f.read()
c = c.replace('alt="Ring"', 'alt="Il Ring"')
with open('il-ring.html', 'w') as f:
    f.write(c)
