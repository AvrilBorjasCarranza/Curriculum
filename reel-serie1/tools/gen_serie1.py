#!/usr/bin/env python3
"""Vídeo 1/6 · VIOLETTE (8 s, 1080x1920): pulpo violeta 3D (assets/pulpo/giro.webm + final.png), siluetas «?» y textos.
Uso: gen_serie1.py <carpeta del proyecto>"""
import os, sys, json
OUT = sys.argv[1]; T = 8.0; SEQ_T = 3.1
CORAL, DBLUE, YEL, VIOLET = "#CD575B", "#1F5F93", "#FFD84D", "#7051C4"
META = json.load(open(os.path.join(OUT, "assets/escena/capas.json")))
def layer(k):
    m = META[k]
    return (f'      <img id="L{k}" class="layer clip" src="assets/escena/capa_{k}.png" alt="" data-start="0" data-duration="{T}" data-track-index="2" '
            f'style="left:{m["left"]}px;top:{m["top"]}px;width:{m["width"]}px;height:{m["height"]}px;transform-origin:{m["ox"]}px {m["oy"]}px;z-index:4" />')
sils = "\n".join(layer(k) for k in ("s1", "s2", "s3", "s4", "s5"))
FULL = 'position:absolute;left:0;top:0;width:1080px;height:1920px;'
def aud(i, f, t, d, tr, v): return f'      <audio id="{i}" class="clip" src="assets/sfx/{f}" data-start="{t}" data-duration="{d}" data-track-index="{tr}" data-volume="{v}"></audio>'
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
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #BAE6FD; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; }}
      .layer {{ position: absolute; display: block; opacity: 0; }}
      .txt {{ position: absolute; left: 0; width: 1080px; text-align: center; font-family: "Bagel Fat One", sans-serif; opacity: 0; color: {DBLUE}; -webkit-text-stroke: 14px #fff; paint-order: stroke fill; line-height: 1.05; }}
      #h1 {{ top: 300px; font-size: 92px; }}
      #h2 {{ top: 300px; font-size: 78px; }}
      #badge {{ top: 250px; font-family: Modak, "Bagel Fat One", sans-serif; font-size: 230px; color: {CORAL}; -webkit-text-stroke: 26px #fff; filter: drop-shadow(0 8px 0 #fff); }}
      #q {{ top: 330px; font-size: 80px; }}
      #cta {{ top: 520px; opacity: 0; }}
      #cta span {{ display: inline-block; font-family: "Bagel Fat One", sans-serif; font-size: 54px; color: {DBLUE}; background: {YEL}; padding: 18px 46px 24px; border-radius: 999px; border: 8px solid #fff; -webkit-text-stroke: 0; }}
      #logo {{ position: absolute; left: 45px; top: 110px; width: 150px; height: 150px; opacity: 0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">
      <div id="bg" class="clip" data-start="0" data-duration="{T}" data-track-index="0" style="{FULL}z-index:1;overflow:hidden"><img src="assets/escena/fondo.png" alt="" style="position:absolute;left:0;top:-780px;width:1080px;height:2700px" /></div>
{sils}
      <video id="pulpo" class="clip" src="assets/pulpo/giro.webm" data-start="0" data-duration="{SEQ_T}" data-track-index="3" muted playsinline style="{FULL}z-index:7"></video>
      <img id="pulpo-fin" class="clip" src="assets/pulpo/final.png" alt="" data-start="{SEQ_T}" data-duration="{round(T - SEQ_T, 3)}" data-track-index="3" style="{FULL}z-index:7" />
      <div id="h1" class="txt clip" data-start="0" data-duration="2.4" data-track-index="4" style="z-index:10">Porte-clés<br>imprimé en 3D</div>
      <div id="h2" class="txt clip" data-start="2.4" data-duration="2.0" data-track-index="4" style="z-index:10">Rêveur. Calme.<br>Un peu timide.</div>
      <div id="badge" class="txt clip" data-start="4.4" data-duration="1.5" data-track-index="4" style="z-index:10">1/6</div>
      <div id="q" class="txt clip" data-start="5.9" data-duration="2.1" data-track-index="4" style="z-index:10">Quel est TON mood ?</div>
      <div id="cta" class="txt clip" data-start="6.3" data-duration="1.7" data-track-index="4" style="z-index:10"><span>Suis-nous pour le 2/6 🐙</span></div>
      <img id="logo" class="clip" src="assets/logo-renardlab.png" alt="RenardLab Impression 3D" data-start="0" data-duration="{T}" data-track-index="4" style="z-index:12" />
      <audio id="music" class="clip" src="assets/bgm/music.mp3" data-start="0" data-duration="{T}" data-track-index="6" data-volume="0.72"></audio>
{aud("p0", "burbuja-pop_doble.mp3", 0.05, 0.65, 7, 0.95)}
{aud("p1", "burbuja-pop_a.mp3", 2.4, 0.34, 8, 0.8)}
{aud("p2", "burbuja-pop_b.mp3", 4.4, 0.34, 9, 0.85)}
{aud("p3", "burbuja-pop_doble.mp3", 6.3, 0.65, 10, 0.9)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.set("#h1", {{ opacity: 1 }}, 0);
      tl.to("#h1", {{ opacity: 0, duration: 0.15 }}, 2.25);
      tl.fromTo("#h2", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, 2.4);
      tl.to("#h2", {{ opacity: 0, duration: 0.15 }}, 4.25);
      [["#Ls1", 4.0], ["#Ls2", 4.1], ["#Ls4", 4.2], ["#Ls5", 4.3], ["#Ls3", 4.45]].forEach(([id, t]) => {{
        tl.fromTo(id, {{ opacity: 0, scale: 0.3 }}, {{ opacity: 1, scale: 1, duration: 0.32, ease: "back.out(2.2)", immediateRender: false }}, t);
      }});
      tl.fromTo("#badge", {{ opacity: 0, scale: 0.4, y: -40 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.4, ease: "back.out(2)" }}, 4.4);
      tl.to("#badge", {{ opacity: 0, duration: 0.15 }}, 5.8);
      tl.fromTo("#q", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, 5.9);
      tl.fromTo("#cta", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }}, 6.3);
      tl.fromTo("#logo", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.7)" }}, 0.2);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(OUT, "index.html"), "w").write(html); print("ok", T)
