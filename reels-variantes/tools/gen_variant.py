#!/usr/bin/env python3
"""Three short loop variants (~8 s) for TikTok/Reels: hook in motion from frame 0, big text, no voice, no music."""
import os, sys

OUT, V = sys.argv[1], sys.argv[2]
INK, YELLOW, ORANGE, CREAM = "#1A1410", "#FFD23F", "#D9500C", "#FFF3E3"

# clips: (file, start, duration); texts: (html, start, end, top px)
VARIANTS = {
    "a": {"clips": [("a1-timelapse.mp4", 0, 4.3), ("a2-plateau.mp4", 4.3, 2.2)],
          "texts": [("REGARDE LES<br><b>BONNETS</b> APPARAÎTRE", 0.0, 2.5, 300),
                    ("IMPRIMÉ EN 3D<br>À <b>METZ</b>", 2.5, 4.3, 300),
                    ("ET TOI, TU METTRAIS<br>QUOI EN <b>FIGURINE</b>&nbsp;?", 4.3, 6.5, 300)]},
    "b": {"clips": [("b1-plaque.mp4", 0, 7.8)],
          "texts": [("LE MOMENT LE PLUS<br><b>SATISFAISANT</b>", 0.0, 3.6, 300),
                    ("D’UNE IMPRESSION<br><b>3D</b>", 3.6, 5.5, 300),
                    ("TU METTRAIS QUOI<br>EN <b>FIGURINE</b>&nbsp;?", 5.5, 7.8, 300)]},
    "c": {"clips": [("c1-impression.mp4", 0, 3.2), ("c2-main.mp4", 3.2, 3.0)],
          "texts": [("POV : TA MASCOTTE<br><b>PREND VIE</b>", 0.0, 3.2, 300),
                    ("DE L’IMPRIMANTE<br>À TA <b>MAIN</b>", 3.2, 6.2, 300)],
          "end": 6.2},
}
cfg = VARIANTS[V]
T = round(cfg.get("end", 0) + 2.6, 2) if "end" in cfg else round(max(s + d for _, s, d in cfg["clips"]), 2)

els, tw = [], []
for i, (f, s, d) in enumerate(cfg["clips"]):
    els.append(f'''      <div id="w{i}" class="wrap" style="z-index:{i + 1}">
        <video id="v{i}" class="clip" src="assets/clips/{f}" data-start="{s}" data-duration="{d}" data-track-index="0" muted playsinline></video>
      </div>''')
    tw.append(f'tl.fromTo("#w{i}", {{ scale: 1.08 }}, {{ scale: 1, duration: 0.5, ease: "power3.out" }}, {s});')
for i, (html, s, e, top) in enumerate(cfg["texts"]):
    els.append(f'''      <div id="t{i}" class="clip" data-start="{s}" data-duration="{round(e - s, 2)}" data-track-index="1" style="z-index:20">
        <div id="t{i}-in" class="txt" style="top:{top}px">{html}</div>
      </div>''')
    tw.append(f'tl.fromTo("#t{i}-in", {{ scale: 0.7, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.18, ease: "back.out(2)" }}, {s + 0.02});')
if "end" in cfg:
    e = cfg["end"]
    els.append(f'''      <div id="endc" class="clip" data-start="{e}" data-duration="{round(T - e, 2)}" data-track-index="0" style="z-index:15">
        <div class="end-bg"></div>
        <img id="end-logo" src="assets/logo-renardlab.png" alt="RenardLab Impression 3D" />
        <div id="end-cta" class="end-cta"><span>TA MASCOTTE ? ÉCRIS-NOUS</span></div>
      </div>''')
    tw += [f'tl.fromTo("#end-logo", {{ scale: 0.5, opacity: 0, rotation: -20 }}, {{ scale: 1, opacity: 1, rotation: 0, duration: 0.5, ease: "back.out(1.6)" }}, {e + 0.03});',
           f'tl.fromTo("#end-cta", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(1.8)" }}, {e + 0.4});']

open(os.path.join(OUT, "index.html"), "w").write(f"""<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {INK}; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; }}
      .wrap {{ position: absolute; inset: 0; }}
      .wrap video {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      .txt {{ position: absolute; left: 60px; width: 960px; text-align: center; font: 400 84px/1.06 "Archivo Black", sans-serif; color: #fff;
        text-shadow: -7px -7px 0 {INK}, 7px -7px 0 {INK}, -7px 7px 0 {INK}, 7px 7px 0 {INK}, 0 14px 30px rgba(0,0,0,.5); }}
      .txt b {{ color: {YELLOW}; font-weight: 400; }}
      .end-bg {{ position: absolute; inset: 0; background: {INK}; }}
      #end-logo {{ position: absolute; left: 270px; top: 420px; width: 540px; height: 540px; }}
      .end-cta {{ position: absolute; left: 0; top: 1040px; width: 1080px; text-align: center; }}
      .end-cta span {{ display: inline-block; background: {ORANGE}; color: #fff; font: 400 54px/1 "Archivo Black", sans-serif; padding: 26px 48px 30px; border-radius: 999px; border: 6px solid {CREAM}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">
{chr(10).join(els)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      {(chr(10) + "      ").join(tw)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
""")
print(V, "duration", T)
