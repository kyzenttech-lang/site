"""Monta os logos do site a partir do K atual (empresa/logo-kyzent/camisas/svg) e do letreiro da marca.
Uso (na raiz do site): python tools/gera_assets.py ../empresa/logo-kyzent tools/letreiro-kyzent.svg assets"""
import os, re, sys

LOGO, LETREIRO_SVG, OUT = sys.argv[1:4]
os.makedirs(os.path.join(OUT, "img"), exist_ok=True)
os.makedirs(os.path.join(OUT, "icons"), exist_ok=True)

def le(nome):
    with open(os.path.join(LOGO, "camisas", "svg", nome), encoding="utf-8") as f:
        return f.read()

def miolo(svg):
    """viewBox e conteúdo interno de um SVG."""
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
    corpo = re.sub(r"^<svg[^>]*>", "", svg.strip())
    corpo = re.sub(r"</svg>$", "", corpo)
    corpo = re.sub(r"<title>.*?</title>", "", corpo)
    return vb, corpo

def com_prefixo(corpo, p):
    """renomeia ids para não colidir quando dois SVGs ficam no mesmo arquivo."""
    ids = set(re.findall(r'id="([^"]+)"', corpo))
    for i in sorted(ids, key=len, reverse=True):
        corpo = corpo.replace(f'id="{i}"', f'id="{p}{i}"').replace(f"url(#{i})", f"url(#{p}{i})")
    return corpo

# letreiro KYZENT (traços próprios da marca, 257 x 40)
with open(LETREIRO_SVG, encoding="utf-8") as f:
    letras = re.search(r'<path d="(M0 0 [^"]+)"', f.read()).group(1)

FONTE = "'Inter','Segoe UI','Helvetica Neue',Arial,sans-serif"

def salva(caminho, s):
    with open(os.path.join(OUT, caminho), "w", encoding="utf-8") as f:
        f.write(s)

def horizontal(arquivo_k, cor_txt, cor_slogan, nome):
    vb, corpo = miolo(le(arquivo_k))
    corpo = com_prefixo(corpo, "h")
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 590 140" width="590" height="140">'
         f'<title>KYZENT</title>'
         f'<svg x="0" y="5" width="270" height="130" viewBox="{vb}">{corpo}</svg>'
         f'<g transform="translate(286 40) scale(1.15)"><path d="{letras}" fill="{cor_txt}"/></g>'
         f'<text x="287" y="109" textLength="294" lengthAdjust="spacing" font-family="{FONTE}" '
         f'font-size="14" font-weight="500" fill="{cor_slogan}">AUTOMAÇÃO &amp; IA</text></svg>')
    salva(f"img/{nome}", s)

horizontal("k-cor-fundo-escuro.svg", "#FFFFFF", "#B8BCC8", "kyzent-horizontal-escuro.svg")
horizontal("k-cor-fundo-claro.svg", "#0B0B0F", "#4A4D57", "kyzent-horizontal-claro.svg")

# K grande (com órbita) para o topo do site
salva("img/kyzent-k.svg", le("k-cor-fundo-escuro.svg"))

# ícone: K sem órbita num quadrado escuro arredondado (favicon e ícone de app)
vb, corpo = miolo(le("k-sem-orbita-escuro.svg"))
icone = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">'
         f'<title>KYZENT</title><rect width="512" height="512" rx="112" fill="#0B0B0F"/>'
         f'<svg x="76" y="96" width="360" height="320" viewBox="{vb}">{com_prefixo(corpo, "i")}</svg></svg>')
salva("icons/icon.svg", icone)
print("ok")
