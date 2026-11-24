#!/usr/bin/env python3
"""Vídeo de la impresión (vertical 1080x1920, 9 s): 0–0,5 s el pulpo ya terminado; después el timelapse acelerado con pops. Uso: gen_impresion.py <carpeta>"""
import os, sys
OUT = sys.argv[1]; T = 9.0
DBLUE, CORAL, YEL = "#1F5F93", "#CD575B", "#FFD84D"
FULL = 'position:absolute;left:0;top:0;width:1080px;height:1920px;'
SPEED = 24.17 / 7.3              # 24 s de clip -> 7,3 s (llena hasta el final)
V0 = 0.5                         # el timelapse empieza a los 0,5 s
def aud(i, f, t, d, tr, v): return f'      <audio id="{i}" class="clip" src="assets/sfx/{f}" data-start="{round(t,2)}" data-duration="{d}" data-track-index="{tr}" data-volume="{v}"></audio>'
# momentos del timelapse (s de clip) y sus pops: base, bolitas, cabeza, anilla
EV = [(0.3, "burbuja-pop_a.mp3"), (7.5, "burbuja-pop_b.mp3"), (13.5, "burbuja-pop_c.mp3"), (20.5, "burbuja-pop_a.mp3")]
sfx = [aud("p0", "burbuja-pop_doble.mp3", 0.02, 0.65, 6, 0.95)] + [aud(f"e{i}", f, V0 + t / SPEED, 0.34, 7 + i, 0.6) for i, (t, f) in enumerate(EV)] + [aud("pend", "burbuja-pop_doble.mp3", V0 + 24 / SPEED - 0.1, 0.65, 12, 0.9)]
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
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #FFE9A0; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #FFE9A0; }}
      .veil {{ position: absolute; left: 0; top: 0; width: 1080px; height: 560px; background: linear-gradient(180deg, rgba(255,233,160,.85) 0%, rgba(255,233,160,0) 100%); z-index: 8; }}
      .txt {{ position: absolute; left: 0; width: 1080px; text-align: center; font-family: "Bagel Fat One", sans-serif; opacity: 0; color: {DBLUE}; -webkit-text-stroke: 14px #fff; paint-order: stroke fill; line-height: 1.05; }}
      #cta {{ position: absolute; left: 0; top: 1560px; width: 1080px; text-align: center; opacity: 0; }}
      #cta span {{ display: inline-block; font-family: "Bagel Fat One", sans-serif; font-size: 54px; color: {DBLUE}; background: #fff; padding: 18px 46px 24px; border-radius: 999px; border: 8px solid {YEL}; }}
      #logo {{ position: absolute; left: 45px; top: 110px; width: 150px; height: 150px; opacity: 0; }}
      .card {{ position: absolute; left: 0; width: 1080px; overflow: hidden; background: #000; border-radius: 0; }}
      .card video, .card img {{ position: absolute; display: block; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">
      <!-- 0–0,5 s: el pulpo terminado (3D) -->
      <img id="ini" class="clip" src="assets/final-3d.png" alt="" data-start="0" data-duration="{V0}" data-track-index="1" style="{FULL}z-index:5;opacity:1" />
      <div id="bgini" class="clip" data-start="0" data-duration="{V0}" data-track-index="0" style="{FULL}z-index:4;background:#BAE6FD"></div>
      <!-- 0,5 s en adelante: timelapse acelerado, recortado a vertical -->
      <video id="v" class="clip" src="assets/impresion-azul.mp4" data-start="{V0}" data-duration="{round(24.17 / SPEED, 2)}" data-track-index="1" data-playback-rate="{SPEED}" muted playsinline style="position:absolute;left:-977px;top:0;width:2720px;height:1920px;z-index:6"></video>
      <div id="bgv" class="clip" data-start="{round(V0 + 24.17 / SPEED, 2)}" data-duration="{round(T - V0 - 24.17 / SPEED, 2)}" data-track-index="1" style="{FULL}z-index:6;background:#BAE6FD"></div>
      <img id="fin3d" class="clip" src="assets/final-3d.png" alt="" data-start="{round(V0 + 24.17 / SPEED, 2)}" data-duration="{round(T - V0 - 24.17 / SPEED, 2)}" data-track-index="2" style="{FULL}z-index:7" />
      <div id="veil" class="veil clip" data-start="{V0}" data-duration="{round(T - V0, 2)}" data-track-index="3"></div>
      <div id="t0" class="txt clip" data-start="{V0}" data-duration="3.2" data-track-index="4" style="top:200px;font-size:88px;z-index:10">Regarde-le<br>naître</div>
      <div id="t1" class="txt clip" data-start="{V0 + 3.4}" data-duration="3.0" data-track-index="4" style="top:230px;font-size:88px;z-index:10">Couche par<br>couche</div>
      <div id="t2" class="txt clip" data-start="{V0 + 6.5}" data-duration="2.0" data-track-index="4" style="top:230px;font-size:88px;z-index:10">1/6 · Violette</div>
      <div id="cta" class="clip" data-start="{V0 + 7.0}" data-duration="{round(T - V0 - 7.0, 2)}" data-track-index="4" style="z-index:10"><span>Suis-nous pour le 2/6 🐙</span></div>
      <img id="logo" class="clip" src="assets/logo-renardlab.png" alt="RenardLab Impression 3D" data-start="0" data-duration="{T}" data-track-index="4" style="z-index:12" />
      <audio id="music" class="clip" src="assets/bgm/music.mp3" data-start="0" data-duration="{T}" data-track-index="5" data-volume="0.7"></audio>
{chr(10).join(sfx)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#t0", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {V0});
      tl.to("#t0", {{ opacity: 0, duration: 0.15 }}, {V0 + 3.05});
      tl.fromTo("#t1", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {V0 + 3.4});
      tl.to("#t1", {{ opacity: 0, duration: 0.15 }}, {V0 + 6.25});
      tl.fromTo("#t2", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {V0 + 6.5});
      tl.fromTo("#cta", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)" }}, {V0 + 7.0});
      tl.fromTo("#logo", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.7)" }}, 0.2);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(OUT, "index.html"), "w").write(html); print("ok", T)
