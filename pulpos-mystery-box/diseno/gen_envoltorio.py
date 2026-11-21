#!/usr/bin/env python3
"""Boceto del envoltorio tipo caramelo (A4 horizontal) y comparación de nombres. Pulpos = bocetos vectoriales provisionales."""
import sys, os
OUT = sys.argv[1]
BLUE, PINK, CREAM, INK = "#BAE6FD", "#FA96CD", "#FEF3C9", "#141414"
DEEP, SHADE = "#2A6FAE", "#7FC2EC"   # azul profundo para textos y azul medio para el volumen: nada de negro en el envoltorio
FONT = "Bagel Fat One"   # texto pequeño; el título usa Modak
SIZES = {"Modak": 22, "Bagel Fat One": 16, "DynaPuff": 15.5, "Titan One": 16.5}
_n = [0]

def grad(hi, mid, lo):
    _n[0] += 1; gid = f"g{_n[0]}"
    return gid, f'<radialGradient id="{gid}" cx="40%" cy="35%" r="72%" fx="34%" fy="26%"><stop offset="0" stop-color="{hi}"/><stop offset=".55" stop-color="{mid}"/><stop offset="1" stop-color="{lo}"/></radialGradient>'

def octo(hi, mid, lo, face="normal", rainbow=False, silhouette=False):
    """Pulpo provisional; coordenadas del render original, viewBox 40 8 440 440."""
    defs, fill = "", {}
    if silhouette:
        body = '<g fill="#161616">' + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in [(115, 328, 58), (410, 328, 58), (262, 195, 180), (196, 358, 66), (330, 358, 66)]) + '</g>'
        q = '<text x="262" y="262" text-anchor="middle" font-family="Bagel Fat One" font-size="170" fill="#FEF3C9">?</text>'
        return f'<svg viewBox="40 8 440 440" xmlns="http://www.w3.org/2000/svg">{body}{q}</svg>'
    parts = {}
    for k in ("side", "dome", "front"):
        if rainbow:
            cols = {"side": ("#FFE27A", "#F6C419", "#C99700"), "dome": ("#FF9AA2", "#FF6F91", "#C83E6B"), "front": ("#9BE08B", "#4CC271", "#2A8F4B")}[k]
        else:
            cols = (hi, mid, lo)
        gid, d = grad(*cols); defs += d; parts[k] = f"url(#{gid})"
    if rainbow:  # cúpula con franjas
        defs += '<linearGradient id="rb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF6F91"/><stop offset=".25" stop-color="#FFB347"/><stop offset=".5" stop-color="#FFE27A"/><stop offset=".75" stop-color="#7EDC8A"/><stop offset="1" stop-color="#6EC1FF"/></linearGradient>'
        parts["dome"] = "url(#rb)"
    s = ''
    s += f'<circle cx="115" cy="328" r="58" fill="{parts["side"]}"/><circle cx="410" cy="328" r="58" fill="{parts["side"]}"/>'
    if rainbow:  # brazo saludando
        for x, y, r in [(440, 250, 40), (462, 190, 36), (470, 135, 32), (462, 85, 30)]:
            s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{parts["side"]}"/>'
        s += '<path d="M505 70 q18 -14 0 -30 M520 80 q26 -22 0 -48" stroke="#141414" stroke-width="7" fill="none" stroke-linecap="round" opacity=".55"/>'
    s += f'<circle cx="262" cy="195" r="180" fill="{parts["dome"]}"/>'
    s += f'<circle cx="196" cy="358" r="66" fill="{parts["front"]}"/><circle cx="330" cy="358" r="66" fill="{parts["front"]}"/>'
    s += '<ellipse cx="170" cy="85" rx="60" ry="34" fill="#fff" opacity=".22" transform="rotate(-28 170 85)"/>'
    eyes = lambda rx=18, ry=26, dy=0: (f'<ellipse cx="183" cy="{177+dy}" rx="{rx}" ry="{ry}" fill="#151515"/><ellipse cx="333" cy="{177+dy}" rx="{rx}" ry="{ry}" fill="#151515"/>'
                                      f'<ellipse cx="177" cy="{165+dy}" rx="5" ry="8" fill="#fff" opacity=".5"/><ellipse cx="327" cy="{165+dy}" rx="5" ry="8" fill="#fff" opacity=".5"/>')
    mouth = '<circle cx="258" cy="224" r="36" fill="#C23B78"/><circle cx="258" cy="224" r="36" fill="none" stroke="#8E1F4D" stroke-width="4"/><circle cx="258" cy="224" r="22" fill="#E0609A"/><circle cx="258" cy="224" r="7" fill="#9C2A5A"/>'
    f = ""
    if face == "normal": f = eyes() + mouth
    elif face == "angry":
        f = eyes(16, 22, 6) + mouth + '<path d="M140 138 L208 166 M376 138 L308 166" stroke="#141414" stroke-width="13" stroke-linecap="round"/>'
        f += '<g stroke="#7A0A12" stroke-width="9" fill="none" stroke-linecap="round"><path d="M360 70 q14 -2 20 -16"/><path d="M400 78 q-2 -14 -16 -20"/><path d="M360 100 q14 2 20 16"/><path d="M400 92 q-2 14 -16 20"/></g>'
    elif face == "cool":
        f = ('<g fill="#141414"><rect x="140" y="150" width="86" height="56" rx="24"/><rect x="290" y="150" width="86" height="56" rx="24"/><rect x="220" y="160" width="76" height="12" rx="6"/></g>'
             '<path d="M156 164 l22 -6 M306 164 l22 -6" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".7"/>') + mouth
    elif face == "sad":
        f = eyes(18, 28, 4) + mouth + '<path d="M140 150 L208 130 M376 150 L308 130" stroke="#141414" stroke-width="10" stroke-linecap="round"/>'
        for x in (172, 344):
            f += f'<path d="M{x} 212 q-20 34 0 52 q20 -18 0 -52z" fill="#7ED3F7" stroke="#2D8FC9" stroke-width="3"/>'
        f += '<ellipse cx="300" cy="330" rx="26" ry="9" fill="#7ED3F7" opacity=".5"/>'
    elif face == "sick":
        import math
        def sp(cx):
            pts = [(cx + (2 + 2.6 * t) * math.cos(t), 177 + (2 + 2.6 * t) * math.sin(t)) for t in [i * 0.25 for i in range(0, 40)]]
            return '<path d="M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + '" stroke="#141414" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        f = sp(183) + sp(333) + mouth.replace("#E0609A", "#C0447F")
        f += '<path d="M258 262 q-10 30 0 48 q12 -16 0 -48z" fill="#9BD86B" stroke="#4E8F23" stroke-width="3"/><path d="M395 120 q-14 22 0 34 q14 -12 0 -34z" fill="#9BE0C6" opacity=".8"/>'
    elif face == "wave":
        f = eyes(17, 25) + mouth + '<path d="M150 135 q33 -22 66 0 M300 135 q33 -22 66 0" stroke="#141414" stroke-width="7" fill="none" stroke-linecap="round" opacity=".0"/>'
    return f'<svg viewBox="40 8 530 440" xmlns="http://www.w3.org/2000/svg"><defs>{defs}</defs>{s}{f}</svg>' if rainbow else f'<svg viewBox="40 8 440 440" xmlns="http://www.w3.org/2000/svg"><defs>{defs}</defs>{s}{f}</svg>'

PINKO  = octo("#FF9CA3", "#E8626E", "#B63A4A")
RED    = octo("#FF6F6F", "#D8262E", "#8E0F1C", "angry")
YELLOW = octo("#FFF08A", "#FFCE2E", "#D69B00", "cool")
BLUE_O = octo("#B8E6FF", "#5EB6F2", "#2C7DBB", "sad")
GREEN  = octo("#C9F59A", "#7FD05A", "#3C9A33", "sick")
RAIN   = octo("", "", "", "wave", rainbow=True)
SIL    = octo("", "", "", silhouette=True)

def pulpo(name, vector):
    """Usa pulpos/<name>.png (render real, fondo transparente) si existe; si no, el dibujo provisional."""
    return f'<img src="pulpos/{name}.png" alt="{name}">' if os.path.exists(os.path.join(OUT, "pulpos", name + ".png")) else vector

PINKO, RED, YELLOW, BLUE_O, GREEN, RAIN = (pulpo(n, v) for n, v in
    [("rosa", PINKO), ("rojo", RED), ("amarillo", YELLOW), ("azul", BLUE_O), ("verde", GREEN), ("arcoiris", RAIN)])

def title(name, size=17):
    return f'<div class="title" style="font-size:{size}mm">{name}</div>'

CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Titan+One&family=Modak&family=Bagel+Fat+One&family=DynaPuff:wght@600;700&family=Inter:wght@500;700&display=swap');
:root {{ --mm: 4px; --f: '{FONT}'; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: Inter, sans-serif; background: #fff; }}
.page {{ position: relative; width: 297mm; height: 210mm; background: #fff; overflow: hidden; }}
.a {{ position: absolute; }}
.title {{ font-family: 'Modak', var(--f), sans-serif; color: {CREAM}; -webkit-text-stroke: 1.8mm #FFFFFF; paint-order: stroke fill; filter: drop-shadow(0 1.2mm 0 #FFFFFF); letter-spacing: .3mm; line-height: 1; white-space: nowrap; display: flex; align-items: center; justify-content: center; height: 24mm; }}
.small {{ font-family: var(--f), sans-serif; color: {CREAM}; -webkit-text-stroke: .7mm #FFFFFF; paint-order: stroke fill; letter-spacing: .15mm; font-size: 4.4mm; line-height: 1.2; text-align: center; }}
.note {{ font-size: 3.1mm; color: #6b6b6b; }}
.panel svg, .panel img {{ width: 100%; height: 100%; display: block; object-fit: contain; }}
.fold {{ border-top: .3mm dashed #3b82c4; }}
.foldv {{ border-left: .3mm dashed #3b82c4; }}
.bubble {{ position: absolute; border-radius: 50%; border: .5mm solid rgba(255,255,255,.9); background: rgba(255,255,255,.35); }}
.pill {{ background: {PINK}; color: {CREAM}; -webkit-text-stroke: .6mm #FFFFFF; paint-order: stroke fill; font-family: var(--f); font-size: 3.6mm; padding: 1mm 3mm; border-radius: 3mm; }}
"""

def bubbles(x0, y0, w, h, seed):
    import random
    r = random.Random(seed); out = ""
    for _ in range(14):
        d = r.choice([3, 4, 5, 7, 9]); x = x0 + r.random() * (w - d); y = y0 + r.random() * (h - d)
        out += f'<div class="bubble" style="left:{x:.1f}mm;top:{y:.1f}mm;width:{d}mm;height:{d}mm"></div>'
    return out

# ---------- hoja plana A4 ----------
X0, Y0 = 31, 20   # origen del envoltorio en la hoja (mm)
def flat(name):
    h = f'<div class="page"><style>{CSS}</style>'
    h += f'<div class="a" style="left:{X0}mm;top:{Y0}mm;width:235mm;height:170mm;background:{BLUE}"></div>'
    h += f'<div class="a" style="left:{X0+220}mm;top:{Y0+45}mm;width:15mm;height:80mm;background:repeating-linear-gradient(135deg,#e7f6ff 0 2mm,#d3eefd 2mm 4mm)"></div>'
    # frente
    h += f'<div class="a" style="left:{X0}mm;top:{Y0+45}mm;width:110mm;height:80mm"><div class="a pill" style="left:4mm;top:71mm">SÉRIE 1</div>'
    h += f'<div class="a" style="left:0;top:2mm;width:110mm">{title(name, 21)}</div>'
    h += f'<div class="a panel" style="left:28mm;top:25mm;width:53mm;height:53mm">{PINKO}</div></div>'
    # dorso
    bx = X0 + 110
    h += f'<div class="a" style="left:{bx}mm;top:{Y0+45}mm;width:110mm;height:80mm">'
    h += f'<div class="a small" style="left:0;top:3mm;width:110mm;font-size:5.6mm">QUEL EST TON MOOD ?</div>'
    row = [RED, YELLOW, BLUE_O, GREEN, SIL]
    for i, o in enumerate(row):
        h += f'<div class="a panel" style="left:{3+i*20.5}mm;top:14mm;width:20mm;height:20mm">{o}</div>'
    h += f'<div class="a panel" style="left:30mm;top:36mm;width:0;height:0"></div>'
    h += f'<div class="a small" style="left:6mm;top:40mm;width:98mm;font-size:4mm">1 PORTE-CLÉS MYSTÈRE PAR BOÎTE</div>'
    h += f'<div class="a small" style="left:6mm;top:49mm;width:98mm;font-size:3.6mm">5 COULEURS + 1 SECRET · SECRET : 1 CHANCE SUR 10</div>'
    h += f'<div class="a small" style="left:6mm;top:62mm;width:98mm;font-size:3.6mm">RenardLab3D · Metz</div>'
    h += f'<div class="a small" style="left:6mm;top:68mm;width:98mm;font-size:3.2mm">@renardlab3d · impression 3D · ~5 cm</div></div>'
    # dobleces
    h += f'<div class="a fold" style="left:{X0-6}mm;top:{Y0+45}mm;width:247mm"></div><div class="a fold" style="left:{X0-6}mm;top:{Y0+125}mm;width:247mm"></div>'
    h += f'<div class="a foldv" style="left:{X0+110}mm;top:{Y0+45}mm;height:80mm"></div><div class="a foldv" style="left:{X0+220}mm;top:{Y0+45}mm;height:80mm"></div>'
    h += f'<div class="a note" style="left:{X0}mm;top:{Y0-8}mm">Boceto A4 horizontal · envoltorio 235 × 170 mm · tubo de ≈ 7 cm de diámetro · - - - dobleces</div>'
    h += f'<div class="a note" style="left:{X0+220}mm;top:{Y0+127}mm">pestaña de pegamento</div>'
    h += f'<div class="a note" style="left:{X0+2}mm;top:{Y0+172}mm">Solapa superior 45 mm · cuerpo 80 mm · solapa inferior 45 mm · los pulpos son bocetos provisionales</div>'
    return h + '</div>'

def front(name, label):
    return (f'<div style="position:relative;width:110mm;height:80mm;background:{BLUE};overflow:hidden">'
            f'<div class="a pill" style="left:4mm;top:71mm">SÉRIE 1</div><div class="a" style="left:0;top:1mm;width:110mm">{title(name, 21)}</div>'
            f'<div class="a panel" style="left:28mm;top:25mm;width:53mm;height:53mm">{PINKO}</div></div>'
            f'<div class="note" style="margin-top:1.5mm;font-size:3.8mm;font-weight:700">{label}</div>')

def compare():
    return (f'<div class="page"><style>{CSS}</style><div class="a" style="left:20mm;top:30mm">{front("OctoMood", "A · OctoMood")}</div>'
            f'<div class="a" style="left:167mm;top:30mm">{front("OctoPlouf", "B · OctoPlouf")}</div>'
            f'<div class="a note" style="left:20mm;top:14mm">Cara frontal: título en Modak, resto en Bagel Fat One, letras en amarillo #FEF3C9 con relieve blanco.</div></div>')

open(os.path.join(OUT, "envoltorio-plano.html"), "w").write(f'<!doctype html><meta charset="utf-8">{flat("OctoMood")}')
open(os.path.join(OUT, "comparacion-nombres.html"), "w").write(f'<!doctype html><meta charset="utf-8">{compare()}')
open(os.path.join(OUT, "personajes.html"), "w").write(f'<!doctype html><meta charset="utf-8"><style>{CSS}</style><div class="page"><div class="a note" style="left:12mm;top:8mm">Los 6 pulpos de la serie: bocetos provisionales para pensar los diseños (solo por color)</div>' + ''.join(f'<div class="a panel" style="left:{10+i*47}mm;top:30mm;width:44mm;height:44mm">{o}</div><div class="a small" style="left:{10+i*47}mm;top:78mm;width:44mm">{t}</div>' for i, (o, t) in enumerate([(PINKO, "ROSA"), (RED, "ROJO"), (YELLOW, "AMARILLO"), (BLUE_O, "AZUL"), (GREEN, "VERDE"), (RAIN, "ARCOÍRIS (SECRETO)")])) + '</div>')
