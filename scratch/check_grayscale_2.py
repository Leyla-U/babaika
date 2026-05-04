import re
import urllib.request
from PIL import Image, ImageStat
import io
import time

html_file = "/Users/leylaudimamedova/babaika/index.html"
with open(html_file, 'r') as f:
    content = f.read()

urls = re.findall(r'src="(https://res\.cloudinary\.com/[^"]+)"', content)
urls = list(set(urls))

for url in urls:
    try:
        if '/video/' in url:
            img_url = url.replace('.mp4', '.jpg')
        else:
            img_url = url
            
        req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img_data = response.read()
        
        try:
            img = Image.open(io.BytesIO(img_data)).convert('RGB')
        except Exception:
            # Maybe webp or something that PIL couldn't identify?
            continue
            
        img_hsv = img.convert('HSV')
        stat_hsv = ImageStat.Stat(img_hsv)
        
        # stat_hsv.extrema[1][1] is max saturation
        # If max sat < 15, it's virtually grayscale
        if stat_hsv.extrema[1][1] < 15:
            print(f"Grayscale: {url}")
            
    except Exception as e:
        pass
