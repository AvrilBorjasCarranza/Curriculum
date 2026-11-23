#!/usr/bin/env python3
"""Vídeo «El nacimiento de Octo» (≈ 11 s, 1080x1920): fondo amarillo; las bolas, el cuerpo, ojos, boca, anilla y los colores aparecen con pops.
Uso: gen_proceso.py <carpeta del proyecto>"""
import os, sys
OUT = sys.argv[1]; T = 11.0
BG, DBLUE, CORAL, YEL = "#FFE9A0", "#1F5F93", "#CD575B", "#FFD84D"
BX, BY = 0, 0   # las capas son pantalla completa
FULL = 'position:absolute;left:0;top:0;width:1080px;height:1920px;'
BALLS = ["cabeza"] + [f"brazo{k}" for k in range(8)]
# (id, archivo, aparece, desaparece, ease) — cada fase sustituye a la anterior con un pop
PH = [("cuerpo", "cuerpo.png", 2.05), ("ojos", "ojos.png", 2.8), ("boca", "boca.png", 3.4), ("anilla", "anilla.png", 4.0),
      ("c1", "col_violeta.png", 4.7), ("c2", "col_rojo.png", 5.9), ("c3", "col_rosa.png", 7.0), ("c4", "col_violeta_rosa.png", 8.1), ("c5", "col_violeta.png", 9.2)]
els, tw = [], []
for i, b in enumerate(BALLS):
    t0 = 0.15 + (0 if i == 0 else 0.45 + 0.17 * i); t1 = 2.05
    els.append(f'      <img id="b{i}" class="clip" src="assets/capas/bola_{b}.png" alt="" data-start="{t0}" data-duration="{round(t1 - t0, 2)}" data-track-index="1" style="{FULL}z-index:3;opacity:0" />')
    tw.append(f'tl.fromTo("#b{i}", {{ opacity: 0, scale: 0.2 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.6)", transformOrigin: "50% 62%" }}, {t0 + 0.0});')
for j, (pid, f, t0) in enumerate(PH):
    t1 = PH[j + 1][2] if j + 1 < len(PH) else T
    els.append(f'      <img id="{pid}" class="clip" src="assets/capas/{f}" alt="" data-start="{t0}" data-duration="{round(t1 - t0 + 0.05, 2)}" data-track-index="1" style="{FULL}z-index:{4 + j};opacity:0" />')
    tw.append(f'tl.fromTo("#{pid}", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.34, ease: "back.out(2.4)", transformOrigin: "50% 62%" }}, {t0});')
# textos: (id, html, inicio, fin, top, tamaño)
TX = [("t0", "8 petites boules.<br>1 pieuvre.", 0.1, 2.0, 300, 88), ("t1", "On les fusionne", 2.05, 2.75, 300, 88), ("t2", "Les yeux…", 2.8, 3.35, 300, 88),
      ("t3", "La bouche…", 3.4, 3.95, 300, 88), ("t4", "L’anneau !", 4.0, 4.65, 300, 88), ("t5", "Et maintenant,<br>les couleurs", 4.7, 7.0, 300, 88),
      ("t6", "Violet", 4.7, 5.85, 1450, 110), ("t7", "Rouge", 5.9, 6.95, 1450, 110), ("t8", "Rose", 7.0, 8.05, 1450, 110), ("t9", "Mix", 8.1, 9.15, 1450, 110),
      ("t10", "Octo<br>violet", 9.2, 11.0, 300, 110)]
for tid, h, a, b, top, fs in TX:
    els.append(f'      <div id="{tid}" class="txt clip" data-start="{a}" data-duration="{round(b - a, 2)}" data-track-index="2" style="top:{top}px;font-size:{fs}px;z-index:20">{h}</div>')
    tw.append(f'tl.fromTo("#{tid}", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, {a});')
els.append(f'      <div id="cta" class="cta clip" data-start="9.5" data-duration="1.5" data-track-index="2" style="z-index:20"><span>Suis-nous pour le 2/6 🐙</span></div>')
tw.append('tl.fromTo("#cta", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }, 9.5);')
tw.append('tl.fromTo("#logo", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.7)" }, 0.2);')
# sonidos: un pop por aparición (los brazos más suaves)
sfx = []; n = 0
def add(t, f, v, d=0.34):
    global n; n += 1; sfx.append(f'      <audio id="s{n}" class="clip" src="assets/sfx/{f}" data-start="{round(t, 2)}" data-duration="{d}" data-track-index="{6 + n % 6}" data-volume="{v}"></audio>')
add(0.15, "burbuja-pop_a.mp3", 0.9)
for i in range(1, 9): add(0.15 + 0.45 + 0.17 * i, ["burbuja-pop_b.mp3", "burbuja-pop_c.mp3"][i % 2], 0.5)
for (pid, f, t0), pf in zip(PH, ["burbuja-pop_doble.mp3", "burbuja-pop_a.mp3", "burbuja-pop_b.mp3", "burbuja-pop_c.mp3", "burbuja-pop_a.mp3", "burbuja-pop_b.mp3", "burbuja-pop_c.mp3", "burbuja-pop_a.mp3", "burbuja-pop_doble.mp3"]):
    add(t0, pf, 0.9, 0.65 if "doble" in pf else 0.34)
html = f"""<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Bagel Fat One"; src: url("assets/fonts/BagelFatOne-latin.woff2") format("woff2"); }}
      @font-face {{ font-family: "Modak"; src: url("assets/fonts/Modak-latin.woff2") format("woff2"); }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {BG}; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: {BG}; }}
      .txt {{ position: absolute; left: 0; width: 1080px; text-align: center; font-family: "Bagel Fat One", sans-serif; opacity: 0; color: {DBLUE}; -webkit-text-stroke: 14px #fff; paint-order: stroke fill; line-height: 1.05; }}
      .cta {{ position: absolute; left: 0; top: 1500px; width: 1080px; text-align: center; opacity: 0; }}
      .cta span {{ display: inline-block; font-family: "Bagel Fat One", sans-serif; font-size: 54px; color: {DBLUE}; background: #fff; padding: 18px 46px 24px; border-radius: 999px; border: 8px solid {YEL}; }}
      #logo {{ position: absolute; left: 45px; top: 110px; width: 150px; height: 150px; opacity: 0; }}
      #sombra {{ position: absolute; left: 270px; top: 1330px; width: 540px; height: 90px; border-radius: 50%; background: radial-gradient(ellipse at center, rgba(120,90,20,.28) 0%, rgba(120,90,20,0) 70%); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">
      <div id="sombra" class="clip" data-start="0" data-duration="{T}" data-track-index="0" style="z-index:2"></div>
{chr(10).join(els)}
      <img id="logo" class="clip" src="assets/logo-renardlab.png" alt="RenardLab Impression 3D" data-start="0" data-duration="{T}" data-track-index="2" style="z-index:25" />
      <audio id="music" class="clip" src="assets/bgm/music.mp3" data-start="0" data-duration="{T}" data-track-index="5" data-volume="0.7"></audio>
{chr(10).join(sfx)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      {(chr(10) + "      ").join(tw)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(OUT, "index.html"), "w").write(html); print("ok", T, "sfx", n)
