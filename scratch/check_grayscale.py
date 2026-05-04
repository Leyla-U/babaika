import re
import urllib.request
from PIL import Image, ImageStat
import io

html_file = "/Users/leylaudimamedova/babaika/index.html"
with open(html_file, 'r') as f:
    content = f.read()

urls = re.findall(r'src="(https://res\.cloudinary\.com/[^"]+)"', content)
urls = list(set(urls))

bw_urls = []
for url in urls:
    try:
        # If it's a video, use the image thumbnail by replacing .mp4 with .jpg
        img_url = url.replace('.mp4', '.jpg')
        req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img_data = response.read()
        
        img = Image.open(io.BytesIO(img_data)).convert('RGB')
        stat = ImageStat.Stat(img)
        
        # Check if R, G, B channels are roughly the same
        # An easy way is to check the variance or difference between channels
        extrema = img.getextrema()
        is_bw = True
        for i in range(len(extrema[0])): # Check a few pixels or just use stat
            pass
            
        # Better: Convert to HSV and check max saturation
        img_hsv = img.convert('HSV')
        stat_hsv = ImageStat.Stat(img_hsv)
        
        # stat_hsv.extrema[1][1] is max saturation
        if stat_hsv.extrema[1][1] < 10:  # Very low max saturation
            bw_urls.append(url)
            print(f"Grayscale: {url}")
        else:
            print(f"Color: {url} (max sat: {stat_hsv.extrema[1][1]})")
    except Exception as e:
        print(f"Error on {url}: {e}")

print("\n--- BW URLs ---")
for u in bw_urls:
    print(u)
