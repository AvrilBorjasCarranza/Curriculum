#!/usr/bin/env python3
"""Prueba de legibilidad: letras amarillas con relieve blanco sobre azul."""
import sys, os
OUT = sys.argv[1]
V = [
 ("A · Tal como lo pediste, pero con el relieve blanco más fino", "#BAE6FD", "#FEF3C9", .9, .3),
 ("B · Mismo amarillo y azul, relieve blanco aún más fino", "#BAE6FD", "#FEF3C9", .5, .15),
 ("C · Letras en un amarillo más intenso (#FFD84D), relieve blanco fino", "#BAE6FD", "#FFD84D", .9, .3),
 ("D · Azul un poco más profundo (#7CCBF4), amarillo #FEF3C9, relieve blanco fino", "#7CCBF4", "#FEF3C9", .9, .3),
]
css = """
@import url('https://fonts.googleapis.com/css2?family=Modak&family=Bagel+Fat+One&family=Inter:wght@500;700&display=swap');
*{box-sizing:border-box;margin:0;padding:0} body{font-family:Inter,sans-serif;background:#fff}
.page{position:relative;width:297mm;height:210mm;overflow:hidden}
.p{position:absolute;width:132mm;height:78mm}
.box{position:absolute;inset:0 0 7mm 0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3mm}
.t{font-family:'Modak';font-size:21mm;line-height:1;white-space:nowrap}
.s{font-family:'Bagel Fat One';font-size:4.4mm;letter-spacing:.15mm;white-space:nowrap}
.l{position:absolute;left:0;bottom:0;font-size:3.3mm;font-weight:700;color:#555}
"""
h = f'<!doctype html><meta charset="utf-8"><style>{css}</style><div class="page">'
for k, (lab, bg, fill, wt, ws) in enumerate(V):
    x, y = 12 + (k % 2) * 140, 10 + (k // 2) * 98
    st = lambda w: f'color:{fill};-webkit-text-stroke:{w}mm #fff;paint-order:stroke fill;'
    h += (f'<div class="p" style="left:{x}mm;top:{y}mm"><div class="box" style="background:{bg}">'
          f'<div class="t" style="{st(wt*2)}filter:drop-shadow(0 .8mm 0 #fff)">OctoMood</div>'
          f'<div class="s" style="{st(ws*2)}">1 PORTE-CLÉS MYSTÈRE PAR BOÎTE</div>'
          f'<div class="s" style="{st(ws*2)}">5 COULEURS + 1 SECRET · SECRET : 1 CHANCE SUR 10</div></div><div class="l">{lab}</div></div>')
open(os.path.join(OUT, "prueba-letras.html"), "w").write(h + '</div>')
