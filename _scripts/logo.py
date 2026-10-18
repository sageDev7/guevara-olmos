"""Logo de Guevara & Olmos desde el archivo en buena calidad (img/logo-buenacalidad-arecortar.png, 2048 px,
colores planos sobre blanco: oro #A77840 en «G O», marrón #835A2F en «&» y en el texto).
Alfa = cuánto se aparta el píxel del blanco; el color se des-premultiplica para que los bordes no queden grises.
Salidas en img/: logo.png (colores originales), logo-claro.png (champagne para fondos oscuros),
monograma.png y monograma-claro.png (solo «G&O»). Uso: python _scripts/logo.py"""
import os
from PIL import Image
D = os.path.join(os.path.dirname(__file__), '..')
src = Image.open(os.path.join(D, 'img', 'logo-buenacalidad-arecortar.png')).convert('RGBA')
bg = Image.new('RGBA', src.size, (255, 255, 255, 255)); bg.alpha_composite(src); im = bg.convert('RGB')
W, H = im.size
px = im.load()
orig = Image.new('RGBA', im.size); claro = Image.new('RGBA', im.size)
po, pc = orig.load(), claro.load()
CH = (240, 214, 170)   # champagne
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        a = (255 - min(r, g, b)) / (255 - 64)
        if a <= 0.02: continue
        a = min(1, a)
        fg = tuple(max(0, min(255, round(255 - (255 - c) / a))) for c in (r, g, b))
        A = round(a * 255)
        po[x, y] = fg + (A,)
        pc[x, y] = tuple(round(f * .35 + h * .65) for f, h in zip(fg, CH)) + (A,)
for n, img in (('logo', orig), ('logo-claro', claro)):
    img = img.crop(img.getbbox())
    img.save(os.path.join(D, 'img', n + '.png'), optimize=True)
    mono = img.crop((0, 0, img.width, int(img.height * .60))); mono = mono.crop(mono.getbbox())   # solo «G&O»
    mono.save(os.path.join(D, 'img', n.replace('logo', 'monograma') + '.png'), optimize=True)
    print(n, img.size, mono.size)
