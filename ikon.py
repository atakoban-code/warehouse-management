import sys, os
from PIL import Image, ImageDraw, ImageChops

src = sys.argv[1]
res = sys.argv[2]
im = Image.open(src).convert("RGBA")
W = im.size[0]
m = Image.new("L", (W * 4, W * 4), 0)
ImageDraw.Draw(m).rounded_rectangle([0, 0, W * 4 - 1, W * 4 - 1], radius=int(W * 4 * 0.125), fill=255)
m = m.resize((W, W), Image.LANCZOS)
im.putalpha(m)

def resize(img, n):
    return img.resize((n, n), Image.LANCZOS)

legacy = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
fore = {"mdpi": 108, "hdpi": 162, "xhdpi": 216, "xxhdpi": 324, "xxxhdpi": 432}
for d, n in legacy.items():
    folder = os.path.join(res, "mipmap-" + d)
    os.makedirs(folder, exist_ok=True)
    resize(im, n).save(os.path.join(folder, "ic_launcher.png"))
    rnd = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    k = int(n * 0.86)
    rnd.paste(resize(im, k), ((n - k) // 2, (n - k) // 2), resize(im, k))
    cm = Image.new("L", (n * 4, n * 4), 0)
    ImageDraw.Draw(cm).ellipse([0, 0, n * 4 - 1, n * 4 - 1], fill=255)
    cm = cm.resize((n, n), Image.LANCZOS)
    rnd.putalpha(ImageChops.multiply(rnd.getchannel("A"), cm))
    rnd.save(os.path.join(folder, "ic_launcher_round.png"))
for d, n in fore.items():
    folder = os.path.join(res, "mipmap-" + d)
    os.makedirs(folder, exist_ok=True)
    cv = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    k = int(n * 0.64)
    small = resize(im, k)
    cv.paste(small, ((n - k) // 2, (n - k) // 2), small)
    cv.save(os.path.join(folder, "ic_launcher_foreground.png"))
vals = os.path.join(res, "values")
os.makedirs(vals, exist_ok=True)
open(os.path.join(vals, "ikon_latar.xml"), "w").write(
    '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ikon_latar">#0124BB</color>\n</resources>\n')
any26 = os.path.join(res, "mipmap-anydpi-v26")
os.makedirs(any26, exist_ok=True)
xml = ('<?xml version="1.0" encoding="utf-8"?>\n'
       '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
       '    <background android:drawable="@color/ikon_latar"/>\n'
       '    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>\n'
       '</adaptive-icon>\n')
for nama in ("ic_launcher.xml", "ic_launcher_round.xml"):
    open(os.path.join(any26, nama), "w").write(xml)
print("ikon selesai")
