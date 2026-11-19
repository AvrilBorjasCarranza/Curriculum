#!/usr/bin/env python3
"""Short RenardLab3D reel (18 s): one real clip per beat, the owner's voice, word captions."""
import json, os, sys, difflib, unicodedata

OUT = sys.argv[1]
NO_MUSIC = bool(os.environ.get("NO_MUSIC"))
WORDS = json.load(open(os.path.join(OUT, "..", "reel-renardlab", "assets", "voice", "words.json")))
T = 18.32
ORANGE, INK, CREAM, YELLOW, RED = "#D9500C", "#1A1410", "#FFF3E3", "#FFD23F", "#C41E1B"

# beats: (id, clip file or None, start, end)
BEATS = [
    ("b1", "c1-ours-plateau.mp4", 0.0, 2.3),
    ("b2", "c2-ours-timelapse.mp4", 2.3, 4.6),
    ("b3", "c3-impression.mp4", 4.6, 6.87),
    ("b4", "c4-mascotte-main.mp4", 6.87, 8.45),
    ("b5", "c5-personnages.mp4", 8.45, 9.73),
    ("b6", "c6-exclusif.mp4", 9.73, 14.87),
    ("b7", None, 14.87, T),
]
# voice lines inside voix-reel-court.mp3: (words.json key, time in the track, cut from this time in the line)
LINES = [("s1", 0.15, 0.0), ("s3", 2.3, 0.0), ("s4a", 6.87, 0.0), ("s4c", 8.45, 0.0), ("s6", 9.73, 1.40), ("s10", 14.87, 0.0)]
CAPS = {
    "s1": ["Le magasin", "d’en face", "copie toutes", "tes idées ?"],
    "s3": ["Chez RenardLab3D,", "on crée des produits", "personnalisés", "en impression 3D", "pour les commerces."],
    "s4a": ["Ta mascotte", "en figurine ?"],
    "s4c": ["Tes propres", "personnages ?"],
    "s6": ["Tu peux nous demander", "de ne pas vendre", "tes créations", "à un concurrent précis.", "Tes produits,", "il ne les aura pas", "chez nous."],
    "s10": ["Écris-nous en DM", "pour commencer."],
}
EMPH = {"copie", "renardlab3d,", "personnalisés", "mascotte", "personnages", "concurrent", "nous.", "dm"}

def norm(x):
    x = unicodedata.normalize("NFD", x.lower())
    return "".join(c for c in x if c.isalnum() and not unicodedata.combining(c))

def align(groups, key, at, cut):
    words = [w for w in WORDS[key]["words"] if w["end"] > cut]
    vd = WORDS[key]["dur"] - cut
    sc, st = [], []
    for w in words:
        n = norm(w["text"]); s0 = max(0, w["start"] - cut); e = max(s0, min(w["end"] - cut, vd))
        for i, c in enumerate(n): sc.append(c); st.append(s0 + (e - s0) * i / max(1, len(n)))
    tbg = []
    for g in groups:
        toks = []
        for x in g.split(" "):
            if not norm(x) and toks: toks[-1] += " " + x
            else: toks.append(x)
        tbg.append(toks)
    flat = [x for tg in tbg for x in tg]
    cc, owner = [], []
    for i, x in enumerate(flat):
        for c in norm(x): cc.append(c); owner.append(i)
    m = {}
    for a, b, size in difflib.SequenceMatcher(None, cc, sc, autojunk=False).get_matching_blocks():
        for j in range(size): m[a + j] = b + j
    times = [None] * len(flat)
    for ci, wi in enumerate(owner):
        if times[wi] is None and ci in m: times[wi] = st[m[ci]]
    known = [i for i, v in enumerate(times) if v is not None]
    for i in range(len(times)):
        if times[i] is None:
            p = max([k for k in known if k < i], default=None); n_ = min([k for k in known if k > i], default=None)
            times[i] = ((times[p] if p is not None else 0.0) + (times[n_] if n_ is not None else vd)) / 2
    for i in range(1, len(times)): times[i] = max(times[i], times[i - 1] + 0.05)
    out, k = [], 0
    for g, tg in zip(groups, tbg):
        wl = [(x, round(at + times[k + j], 3)) for j, x in enumerate(tg)]; k += len(tg)
        out.append({"start": round(wl[0][1] - 0.06, 3), "words": wl})
    for i, g in enumerate(out):
        g["end"] = round(out[i + 1]["start"] - 0.03, 3) if i + 1 < len(out) else round(at + vd + 0.15, 3)
    return out

groups = []
for key, at, cut in LINES: groups += align(CAPS[key], key, at, cut)

# ---------------------------------------------------------------- captions sub-composition
gh = []
for i, g in enumerate(groups):
    ws = " ".join(f'<span class="cw{" emph" if w.lower().strip("?!.,") in EMPH or w.lower() in EMPH else ""}" data-t="{t}">{w.upper()}</span>' for w, t in g["words"])
    gh.append(f'    <div id="cap-{i}" class="cap-group clip" data-start="{g["start"]}" data-duration="{round(g["end"] - g["start"], 3)}" data-track-index="0">{ws}</div>')
open(os.path.join(OUT, "compositions", "captions.html"), "w").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .cap-group {{ position: absolute; left: 90px; top: 1090px; width: 900px; height: 200px; display: flex; flex-wrap: wrap; align-content: center; justify-content: center; column-gap: 0.36em; row-gap: 0.05em; text-align: center; overflow: visible; font-family: "Archivo Black", sans-serif; line-height: 1.05; }}
    .cw {{ display: inline-block; color: #FFFFFF; text-shadow: -5px -5px 0 {INK}, 5px -5px 0 {INK}, -5px 5px 0 {INK}, 5px 5px 0 {INK}, 0 -6px 0 {INK}, 0 6px 0 {INK}, -6px 0 0 {INK}, 6px 0 0 {INK}, 0 12px 22px rgba(0,0,0,0.45); }}
    .cw.emph {{ color: {YELLOW}; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(gh)}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      const fit = (window.__hyperframes && window.__hyperframes.fitTextFontSize) || null;
      document.querySelectorAll("#root .cap-group").forEach((g) => {{
        let size = 88;
        if (fit) size = Math.max(58, Math.min(88, fit(g.textContent, {{ fontFamily: "Archivo Black", fontWeight: 400, maxWidth: 840, baseFontSize: 88, minFontSize: 58 }}).fontSize));
        g.style.fontSize = size + "px";
        g.querySelectorAll(".cw").forEach((w) => {{
          const t = parseFloat(w.dataset.t), big = w.classList.contains("emph");
          tl.fromTo(w, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.04, ease: "none" }}, t);
          tl.fromTo(w, {{ scale: 0.55, y: 18 }}, {{ scale: big ? 1.12 : 1, y: 0, duration: 0.16, ease: "back.out(2.2)" }}, t);
          if (big) tl.to(w, {{ scale: 1, duration: 0.2, ease: "power2.out" }}, t + 0.16);
        }});
      }});
      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
""")

# ---------------------------------------------------------------- root
clips, tweens = [], []
for i, (bid, f, a, b) in enumerate(BEATS):
    if not f: continue
    clips.append(f'''      <div id="{bid}-wrap" class="wrap" style="z-index:{i + 1}">
        <video id="{bid}" class="clip" src="assets/clips/{f}" data-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="0" muted playsinline></video>
      </div>''')
    tweens.append(f'tl.fromTo("#{bid}-wrap", {{ scale: 1.1 }}, {{ scale: 1, duration: 0.45, ease: "power3.out" }}, {a});')
b6a, b6b = BEATS[5][2], BEATS[5][3]
b7a = BEATS[6][2]
overlays = f'''      <div id="hook" class="clip" data-start="0" data-duration="2.3" data-track-index="2" style="z-index:20">
        <div id="hook-t" class="hook">TON CONCURRENT<br><b>COPIE</b> TES&nbsp;IDÉES&nbsp;?</div>
      </div>
      <div id="excl" class="clip" data-start="{b6a}" data-duration="{round(b6b - b6a, 3)}" data-track-index="2" style="z-index:20">
        <div id="excl-t" class="excl"><span>EXCLUSIF</span></div>
        <div id="excl-s" class="excl-s">RÉSERVÉ À TA BOUTIQUE</div>
      </div>
      <div id="end" class="clip" data-start="{b7a}" data-duration="{round(T - b7a, 3)}" data-track-index="0" style="z-index:15">
        <div class="end-bg"></div>
        <img id="end-logo" src="assets/logo-renardlab.png" alt="RenardLab Impression 3D" />
        <div id="end-sub" class="end-sub">IMPRESSION 3D PERSONNALISÉE · METZ</div>
        <div id="end-cta" class="end-cta"><span>ÉCRIS-NOUS EN DM</span></div>
      </div>'''
tweens += [
    'tl.fromTo("#hook-t", { scale: 0.7, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.18, ease: "back.out(2)" }, 0.02);',
    f'tl.fromTo("#excl-t", {{ scale: 2.2, opacity: 0, rotation: -12 }}, {{ scale: 1, opacity: 1, rotation: -6, duration: 0.25, ease: "power4.in" }}, {b6a + 0.3});',
    f'tl.fromTo("#excl-s", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, {b6a + 0.7});',
    f'tl.fromTo("#end-logo", {{ scale: 0.5, opacity: 0, rotation: -20 }}, {{ scale: 1, opacity: 1, rotation: 0, duration: 0.55, ease: "back.out(1.6)" }}, {b7a + 0.05});',
    f'tl.fromTo("#end-sub", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {b7a + 0.4});',
    f'tl.fromTo("#end-cta", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(1.8)" }}, {b7a + 0.55});',
]
audio = [f'      <audio id="voice" class="clip" src="assets/voice/voix-reel-court.mp3" data-start="0" data-duration="{T}" data-track-index="5" data-volume="1"></audio>']
if not NO_MUSIC:
    audio.append(f'      <audio id="music" class="clip" src="assets/bgm/music.mp3" data-start="0" data-duration="{T}" data-track-index="6" data-volume="0.18"></audio>')

index = f"""<!doctype html>
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
      .hook {{ position: absolute; left: 60px; top: 330px; width: 960px; text-align: center; font: 400 80px/1.06 "Archivo Black", sans-serif; color: #fff;
        text-shadow: -7px -7px 0 {INK}, 7px -7px 0 {INK}, -7px 7px 0 {INK}, 7px 7px 0 {INK}, 0 14px 30px rgba(0,0,0,.5); }}
      .hook b {{ color: {YELLOW}; font-weight: 400; }}
      .excl {{ position: absolute; left: 0; top: 380px; width: 1080px; text-align: center; }}
      .excl span {{ display: inline-block; font: 400 130px/1 "Archivo Black", sans-serif; color: {RED}; border: 14px solid {RED}; padding: 18px 40px 26px; border-radius: 20px; background: {CREAM}; }}
      .excl-s {{ position: absolute; left: 0; top: 640px; width: 1080px; text-align: center; font: 400 56px/1.1 "Archivo Black", sans-serif; color: #fff;
        text-shadow: -5px -5px 0 {INK}, 5px -5px 0 {INK}, -5px 5px 0 {INK}, 5px 5px 0 {INK}; }}
      .end-bg {{ position: absolute; inset: 0; background: {INK}; }}
      #end-logo {{ position: absolute; left: 290px; top: 300px; width: 500px; height: 500px; }}
      .end-sub {{ position: absolute; left: 0; top: 830px; width: 1080px; text-align: center; font: 900 40px/1.2 Inter, sans-serif; letter-spacing: .1em; color: {CREAM}; opacity: .85; }}
      .end-cta {{ position: absolute; left: 0; top: 920px; width: 1080px; text-align: center; }}
      .end-cta span {{ display: inline-block; background: {ORANGE}; color: #fff; font: 400 62px/1 "Archivo Black", sans-serif; padding: 26px 56px 30px; border-radius: 999px; border: 6px solid {CREAM}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920">
{chr(10).join(clips)}
{overlays}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{T}" data-track-index="3" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:30"></div>
{chr(10).join(audio)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      {chr(10) + "      ".join(tweens)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)
open(os.path.join(OUT, "index.html"), "w").write(index)
for g in groups: print(g["start"], g["end"], " ".join(w for w, _ in g["words"]))
