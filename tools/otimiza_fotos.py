"""Gera versões AVIF e WebP das fotos (o JPG continua como reserva para navegadores antigos).
Uso (na raiz do site): python tools/otimiza_fotos.py
Cada foto sai em duas larguras: 640 px (celular) e 1200 px (computador)."""
import os
from PIL import Image

PASTA = os.path.join("assets", "fotos")
LARGURAS = (640, 1200)

for nome in sorted(os.listdir(PASTA)):
    if not nome.lower().endswith(".jpg"):
        continue
    base = os.path.splitext(nome)[0]
    with Image.open(os.path.join(PASTA, nome)) as foto:
        foto = foto.convert("RGB")
        for larg in LARGURAS:
            if foto.width < larg and larg != LARGURAS[0]:
                larg = foto.width
            alt = round(foto.height * larg / foto.width)
            menor = foto.resize((larg, alt), Image.LANCZOS) if foto.width > larg else foto
            menor.save(os.path.join(PASTA, f"{base}-{larg}.avif"), quality=50)
            menor.save(os.path.join(PASTA, f"{base}-{larg}.webp"), quality=72, method=6)
    print("ok", base)
