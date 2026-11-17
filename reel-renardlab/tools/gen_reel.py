#!/usr/bin/env python3
"""Generates the RenardLab3D reel (HyperFrames project): scenes, captions, index.html."""
import json, math, os, sys

OUT = sys.argv[1]
os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)

BAR = 60 / 130 * 4  # 1.846 s, music at 130 bpm
def bar(n): return round(n * BAR, 3)

ORANGE, ORANGE_D, CREAM, INK = "#FF6B1A", "#D9500C", "#FFF3E3", "#1A1410"
YELLOW, RED, GREEN, SLATE, NAVY, XMAS = "#FFD23F", "#E8322F", "#1F8A4C", "#2E333B", "#14304A", "#A3192A"

# ---------------------------------------------------------------- scenes: id, start bar, end bar, ground
SCENES = [
    ("s1-hook", 0, 2, CREAM), ("s2-reste", 2, 3, INK), ("s3-marque", 3, 6, ORANGE),
    ("s4-produits", 6, 9, CREAM), ("s5-ensemble", 9, 12, INK), ("s6-exclu", 12, 17, SLATE),
    ("s7-facile", 17, 20, CREAM), ("s8-noel", 20, 23, XMAS), ("s9-france", 23, 26, NAVY),
    ("s10-dm", 26, 28, ORANGE), ("s11-partage", 28, 30.5, INK),
]
TOTAL = bar(30.5)  # 56.308 s

# ---------------------------------------------------------------- captions (the script, verbatim)
CAPS = {
    "s1-hook": ["Le magasin", "d’en face", "copie toutes", "tes idées ?"],
    "s2-reste": ["Si tu as", "un commerce,", "reste."],
    "s3-marque": ["Chez RenardLab3D,", "on crée des produits", "personnalisés", "en impression 3D", "pour les commerces."],
    "s4a": ["Ta mascotte", "en figurine ?"], "s4b": ["Ton logo", "en porte-clés ?"], "s4c": ["Tes propres", "personnages ?"],
    "s5-ensemble": ["On imagine", "tes produits", "avec toi", "et on les réalise", "selon tes envies."],
    "s6-exclu": ["Et le magasin", "d’en face ?", "Tu peux nous demander", "de ne pas vendre", "tes créations", "à un concurrent précis.", "Tes produits,", "il ne les aura pas", "chez nous."],
    "s7-facile": ["Tu n’y connais rien", "en impression 3D ?", "Pas de problème.", "Tu nous donnes", "ton idée,", "on s’occupe du reste."],
    "s8-noel": ["Et pour Noël,", "pourquoi ne pas proposer", "tes propres créations", "à tes clients ?"],
    "s9-france": ["Remise en main propre", "à Metz", "et livraison", "partout en France,", "toute l’année."],
    "s10-dm": ["Écris-nous", "en DM", "pour commencer."],
    "s11-partage": ["Et envoie cette vidéo", "à un commerçant", "qui pourrait", "en avoir besoin !"],
}
# emphasis words (highlighted yellow and slightly larger)
EMPH = {"copie", "reste.", "renardlab3d,", "personnalisés", "figurine", "porte-clés", "personnages", "toi",
        "concurrent", "nous.", "problème.", "reste.", "noël,", "metz", "france,", "dm", "commerçant"}

WINDOWS = {
    "s1-hook": (0.12, bar(2) - 0.12), "s2-reste": (bar(2) + 0.08, bar(3) - 0.05),
    "s3-marque": (bar(3) + 0.25, bar(6) - 0.3),
    "s4a": (bar(6) + 0.1, bar(7) - 0.1), "s4b": (bar(7) + 0.1, bar(8) - 0.1), "s4c": (bar(8) + 0.1, bar(9) - 0.15),
    "s5-ensemble": (bar(9) + 0.2, bar(12) - 0.3), "s6-exclu": (bar(12) + 0.2, bar(17) - 0.3),
    "s7-facile": (bar(17) + 0.15, bar(20) - 0.35), "s8-noel": (bar(20) + 0.3, bar(23) - 0.3),
    "s9-france": (bar(23) + 0.25, bar(26) - 0.3), "s10-dm": (bar(26) + 0.2, bar(28) - 0.35),
    "s11-partage": (bar(28) + 0.15, bar(28) + 2.75),
}

def time_groups(groups, w0, w1, gap=0.06):
    weights = [len(g) + 6 for g in groups]
    span = w1 - w0 - gap * (len(groups) - 1)
    out, t = [], w0
    for g, wt in zip(groups, weights):
        d = span * wt / sum(weights)
        words = g.split(" ")
        ww = [len(x) + 2 for x in words]
        wt_t, wl = t, []
        for x, k in zip(words, ww):
            wd = d * 0.8 * k / sum(ww)  # words arrive over the first 80 % of the group
            wl.append((x, round(wt_t, 3)))
            wt_t += wd
        out.append({"text": g, "start": round(t, 3), "end": round(t + d, 3), "words": wl})
        t += d + gap
    return out

CAPTION_TIMES = {k: time_groups(v, *WINDOWS[k]) for k, v in CAPS.items()}

# ---------------------------------------------------------------- shared scene scaffolding
PRELUDE = """
      const tl = gsap.timeline({ paused: true });
      const D = __D__;
      const ST = "#__ID__-stage";
      const whipIn = () => tl.fromTo(ST, { x: 760, filter: "blur(18px)" }, { x: 0, filter: "blur(0px)", duration: 0.3, ease: "power3.out" }, 0);
      const whipOut = () => tl.fromTo(ST, { x: 0, filter: "blur(0px)" }, { x: -760, filter: "blur(18px)", duration: 0.2, ease: "power3.in", immediateRender: false }, D - 0.2);
      const blurIn = (d = 0.2) => tl.fromTo(ST, { opacity: 0, filter: "blur(10px)", scale: 1.04 }, { opacity: 1, filter: "blur(0px)", scale: 1, duration: d, ease: "power2.out" }, 0);
      const blurOut = () => tl.fromTo(ST, { opacity: 1, filter: "blur(0px)" }, { opacity: 0, filter: "blur(8px)", duration: 0.18, ease: "power2.in", immediateRender: false }, D - 0.18);
      const irisIn = (x, y) => tl.fromTo(ST, { clipPath: `circle(0px at ${x}px ${y}px)` }, { clipPath: `circle(2300px at ${x}px ${y}px)`, duration: 0.42, ease: "power3.in" }, 0);
      const pop = (sel, at, from = 0.4) => tl.fromTo(sel, { scale: from, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.7)" }, at);
      const draw = (sel, at, d = 0.6, ease = "power2.inOut") => tl.fromTo(sel, { strokeDashoffset: 2000 }, { strokeDashoffset: 0, duration: d, ease }, at);
"""

def prelude_for(js, dur, sid):
    lines = PRELUDE.replace("__D__", str(dur)).replace("__ID__", sid).split("\n")
    keep = []
    for ln in lines:
        m = ln.strip()
        if m.startswith("const ") and "=>" in m:
            name = m.split()[1]
            if name + "(" not in js: continue
        keep.append(ln)
    return "\n".join(keep)

def scene_file(sid, dur, ground, root_bg, css, html, js):
    return f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; background: {root_bg}; font-family: "Archivo Black", sans-serif; }}
    #{sid}-stage {{ position: absolute; inset: 0; }}
    #{sid}-ground {{ position: absolute; inset: 0; background: {ground}; }}
    .{sid}-svg {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }}
    .dash {{ stroke-dasharray: 2000; stroke-dashoffset: 2000; }}
    .chip {{ position: absolute; font-family: "Archivo Black", sans-serif; text-transform: uppercase; letter-spacing: 0.02em; border-radius: 999px; padding: 14px 30px 16px; white-space: nowrap; }}
{css}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div id="{sid}-stage">
      <div id="{sid}-ground"></div>
{html}
    </div>
  </div>
  <script>
    (function () {{
{prelude_for(js, dur, sid)}
{js}
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
"""

# ---------------------------------------------------------------- drawing helpers (SVG strings)
def shop(gid, x, y, w, awning, label, body=CREAM, stroke=INK, label_col=None):
    label_col = label_col or (INK if awning == ORANGE else CREAM)
    h = 420
    stripes = "".join(
        f'<rect x="{x + i * w / 6:.1f}" y="{y + 40}" width="{w / 6 + 0.5:.1f}" height="80" fill="{awning if i % 2 == 0 else CREAM}"/>'
        for i in range(6))
    scallops = "".join(
        f'<circle cx="{x + w / 12 + i * w / 6:.1f}" cy="{y + 120}" r="{w / 12:.1f}" fill="{awning if i % 2 == 0 else CREAM}" stroke="{stroke}" stroke-width="6"/>'
        for i in range(6))
    return f'''<g id="{gid}">
        <rect x="{x}" y="{y + 100}" width="{w}" height="{h - 100}" fill="{body}" stroke="{stroke}" stroke-width="8" rx="6"/>
        <rect x="{x - 14}" y="{y - 30}" width="{w + 28}" height="76" fill="{awning}" stroke="{stroke}" stroke-width="8" rx="10"/>
        <text x="{x + w / 2}" y="{y + 22}" text-anchor="middle" font-family="Archivo Black" font-size="40" fill="{label_col}">{label}</text>
        {stripes}{scallops}
        <rect x="{x}" y="{y + 40}" width="{w}" height="80" fill="none" stroke="{stroke}" stroke-width="8"/>
        <rect x="{x + 30}" y="{y + 200}" width="{w * 0.45:.0f}" height="160" fill="#BFE3F2" stroke="{stroke}" stroke-width="8" rx="6"/>
        <rect x="{x + w * 0.62:.0f}" y="{y + 190}" width="{w * 0.28:.0f}" height="{h - 190}" fill="{awning}" stroke="{stroke}" stroke-width="8" rx="4"/>
        <circle cx="{x + w * 0.66:.0f}" cy="{y + 310}" r="7" fill="{stroke}"/>
      </g>'''

def bulb(gid, cx, cy, s=1.0, col=YELLOW):
    return f'''<g transform="translate({cx} {cy}) scale({s})"><g id="{gid}">
        <circle cx="0" cy="0" r="92" fill="{col}" opacity="0.28"/>
        <path d="M-46 10 A58 58 0 1 1 46 10 C34 28 26 38 24 58 L-24 58 C-26 38 -34 28 -46 10 Z" fill="{col}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
        <rect x="-26" y="58" width="52" height="16" rx="4" fill="{INK}"/><rect x="-20" y="78" width="40" height="12" rx="4" fill="{INK}"/>
        <path d="M-14 28 L-6 -6 L6 -6 L14 28" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
      </g></g>'''

def star_path(cx, cy, R, r, n=5):
    pts = []
    for i in range(n * 2):
        a = -math.pi / 2 + i * math.pi / n
        rad = R if i % 2 == 0 else r
        pts.append(f"{cx + rad * math.cos(a):.1f},{cy + rad * math.sin(a):.1f}")
    return "M" + " L".join(pts) + " Z"

# ---------------------------------------------------------------- S1 hook
def s1(d):
    sid = "s1-hook"
    html = f'''      <svg class="{sid}-svg" viewBox="0 0 1080 1920">
        <rect x="0" y="1010" width="1080" height="16" fill="{INK}" opacity="0.15"/>
        {shop("s1-shop-a", 80, 560, 400, ORANGE, "TOI")}
        {shop("s1-shop-b", 600, 560, 400, "#5E6068", "EN FACE")}
        <path id="s1-arc" class="dash" d="M300 400 C 420 250, 660 250, 790 380" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round" stroke-dasharray="22 20"/>
        <path id="s1-arrowhead" d="M760 330 L800 392 L730 395" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
        {bulb("s1-bulb-a", 280, 420)}
        {bulb("s1-bulb-b", 800, 420, 1.0, "#E6E6EA")}
      </svg>
      <div id="s1-stamp" class="chip" style="left:620px;top:780px;background:{RED};color:{CREAM};font-size:58px;border:6px solid {INK};">COPIÉ !</div>
'''
    css = ""
    js = f'''
      tl.fromTo("#s1-bulb-a", {{ scale: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, transformOrigin: "50% 50%", duration: 0.5, ease: "back.out(2)" }}, 0.15);
      tl.fromTo("#s1-arc", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, 0.75);
      tl.fromTo("#s1-arc", {{ strokeDashoffset: 420 }}, {{ strokeDashoffset: 0, duration: 0.55, ease: "power2.inOut" }}, 0.75);
      tl.fromTo("#s1-arrowhead", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1 }}, 1.25);
      tl.fromTo("#s1-bulb-b", {{ scale: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, transformOrigin: "50% 50%", duration: 0.45, ease: "back.out(2)" }}, 1.3);
      tl.fromTo("#s1-stamp", {{ scale: 2.4, rotation: -24, opacity: 0 }}, {{ scale: 1, rotation: -10, opacity: 1, duration: 0.28, ease: "power4.in" }}, 1.85);
      tl.fromTo("#s1-shop-b", {{ x: 0 }}, {{ x: 10, duration: 0.05, yoyo: true, repeat: 3, ease: "none" }}, 2.13);
      whipOut();
'''
    return scene_file(sid, d, CREAM, CREAM, css, html, js)

# ---------------------------------------------------------------- S2 reste
def s2(d):
    sid = "s2-reste"
    html = f'''      <svg class="{sid}-svg" viewBox="0 0 1080 1920">
        {shop("s2-shop", 300, 560, 480, ORANGE, "TON COMMERCE")}
        <g id="s2-sign">
          <line x1="540" y1="700" x2="470" y2="790" stroke="{INK}" stroke-width="5"/><line x1="540" y1="700" x2="610" y2="790" stroke="{INK}" stroke-width="5"/>
          <rect x="420" y="790" width="240" height="96" rx="14" fill="{GREEN}" stroke="{INK}" stroke-width="7"/>
          <text x="540" y="856" text-anchor="middle" font-family="Archivo Black" font-size="44" fill="{CREAM}">OUVERT</text>
        </g>
        <circle id="s2-flood" cx="540" cy="838" r="40" fill="{ORANGE}"/>
      </svg>
'''
    js = f'''
      whipIn();
      tl.fromTo("#s2-sign", {{ rotation: -38, svgOrigin: "540 700" }}, {{ rotation: 0, svgOrigin: "540 700", duration: 1.0, ease: "elastic.out(1, 0.45)" }}, 0.15);
      tl.fromTo("#s2-flood", {{ scale: 0, svgOrigin: "540 838" }}, {{ scale: 40, svgOrigin: "540 838", duration: 0.45, ease: "power2.in" }}, D - 0.45);
'''
    return scene_file(sid, d, INK, INK, "", html, js)

# ---------------------------------------------------------------- S3 brand + printer
LAYERS = [300, 290, 250, 200, 170, 158, 168, 196, 226, 240, 232, 206, 168, 122, 76, 34]
def s3(d):
    sid = "s3-marque"
    lay = []
    for i, w in enumerate(LAYERS):
        y = 976 - i * 26
        lay.append(f'<rect class="s3-layer" id="s3-l{i}" x="{540 - w / 2}" y="{y}" width="{w}" height="26" rx="6" fill="{CREAM}" stroke="{ORANGE_D}" stroke-width="3"/>')
    html = f'''      <div id="s3-word" style="position:absolute;left:0;top:300px;width:1080px;text-align:center;font-size:118px;color:{CREAM};letter-spacing:-0.02em;">
        {"".join(f'<span class="s3-ch" style="display:inline-block">{c}</span>' for c in "RenardLab")}<span class="s3-ch" style="display:inline-block;color:{INK}">3D</span>
      </div>
      <div id="s3-sub" style="position:absolute;left:0;top:445px;width:1080px;text-align:center;font-family:Inter;font-weight:900;font-size:36px;letter-spacing:0.18em;color:{INK};">IMPRESSION 3D · METZ</div>
      <svg class="{sid}-svg" viewBox="0 0 1080 1920">
        <rect x="200" y="520" width="34" height="520" rx="8" fill="{INK}"/><rect x="846" y="520" width="34" height="520" rx="8" fill="{INK}"/>
        <rect x="190" y="1002" width="700" height="40" rx="10" fill="{INK}"/>
        <rect x="320" y="990" width="440" height="14" rx="4" fill="#3A2C22"/>
        <g id="s3-objwrap"><g id="s3-obj">{"".join(lay)}</g></g>
        <g id="s3-gantry">
          <rect x="216" y="560" width="648" height="22" rx="8" fill="{INK}"/>
          <g id="s3-head">
            <rect x="490" y="536" width="100" height="70" rx="12" fill="{CREAM}" stroke="{INK}" stroke-width="7"/>
            <path d="M520 606 L560 606 L548 640 L532 640 Z" fill="{INK}"/>
          </g>
        </g>
      </svg>
'''
    # gantry: head tip at y 640 when gantry y=0; layer i top at 976-26i -> gantry offset = (976-26i) - 640
    js_lines = ['''
      tl.fromTo(".s3-ch", { opacity: 0, y: 40, filter: "blur(6px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.25, stagger: 0.04, ease: "power4.out" }, 0.1);
      tl.fromTo("#s3-sub", { opacity: 0 }, { opacity: 1, duration: 0.25, ease: "power2.out" }, 0.6);''']
    t0, step = 0.9, 0.2
    for i, w in enumerate(LAYERS):
        t = t0 + i * step
        dy = (976 - i * 26) - 640 + 4
        left = i % 2 == 0
        x_from, x_to = (-w / 2, w / 2) if left else (w / 2, -w / 2)
        IR = "" if i == 0 else ", immediateRender: false"
        js_lines.append(
            f'      tl.fromTo("#s3-gantry", {{ y: {dy if i == 0 else dy + 26} }}, {{ y: {dy}, duration: 0.04, ease: "none"{IR} }}, {t:.3f});\n'
            f'      tl.fromTo("#s3-head", {{ x: {x_from:.0f} }}, {{ x: {x_to:.0f}, duration: {step - 0.02:.3f}, ease: "none"{IR} }}, {t:.3f});\n'
            f'      tl.fromTo("#s3-l{i}", {{ scaleX: 0, transformOrigin: "{"left" if left else "right"} center" }}, {{ scaleX: 1, transformOrigin: "{"left" if left else "right"} center", duration: {step - 0.02:.3f}, ease: "none" }}, {t:.3f});')
    end_print = t0 + len(LAYERS) * step
    js_lines.append(f'''
      tl.fromTo("#s3-gantry", {{ y: {(976 - 15 * 26) - 640 + 4} }}, {{ y: -60, duration: 0.4, ease: "power3.out", immediateRender: false }}, {end_print:.3f});
      tl.fromTo("#s3-obj", {{ scale: 1, svgOrigin: "540 840" }}, {{ scale: 14, svgOrigin: "540 840", duration: 0.4, ease: "power3.in" }}, D - 0.4);
      tl.fromTo("#s3-word, #s3-sub", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.2, ease: "power2.in", immediateRender: false }}, D - 0.4);''')
    return scene_file(sid, d, ORANGE, ORANGE, "", html, "\n".join(js_lines)), end_print

# ---------------------------------------------------------------- S4 products (3 beats)
def s4(d):
    sid = "s4-produits"
    fig = f'''<g id="s4-fig">
        <ellipse cx="540" cy="960" rx="230" ry="46" fill="{INK}"/><ellipse cx="540" cy="944" rx="230" ry="46" fill="#3A2C22"/>
        <path d="M420 940 C 400 800, 440 700, 540 690 C 640 700, 680 800, 660 940 Z" fill="{ORANGE}" stroke="{INK}" stroke-width="8"/>
        <path d="M490 940 C 480 840, 500 770, 540 760 C 580 770, 600 840, 590 940 Z" fill="{CREAM}" stroke="{INK}" stroke-width="6"/>
        <path d="M380 470 L420 330 L480 430 Z" fill="{ORANGE}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
        <path d="M700 470 L660 330 L600 430 Z" fill="{ORANGE}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
        <path d="M400 460 C 400 400, 680 400, 680 460 C 690 560, 620 650, 540 700 C 460 650, 390 560, 400 460 Z" fill="{ORANGE}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
        <path d="M455 560 C 500 600, 520 640, 540 700 C 560 640, 580 600, 625 560 C 590 590, 490 590, 455 560 Z" fill="{CREAM}"/>
        <circle cx="490" cy="520" r="16" fill="{INK}"/><circle cx="590" cy="520" r="16" fill="{INK}"/>
        <path d="M526 668 L554 668 L540 690 Z" fill="{INK}"/>
        {"".join(f'<line x1="430" y1="{y}" x2="650" y2="{y}" stroke="{INK}" stroke-width="2" opacity="0.18"/>' for y in range(720, 940, 22))}
      </g>'''
    key = f'''<g id="s4-key">
        <circle cx="540" cy="420" r="70" fill="none" stroke="#9AA0A6" stroke-width="18"/>
        <rect x="528" y="480" width="24" height="70" rx="8" fill="#9AA0A6"/>
        <g id="s4-tag">
          <rect x="350" y="540" width="380" height="420" rx="60" fill="{ORANGE}" stroke="{INK}" stroke-width="10"/>
          <circle cx="540" cy="600" r="20" fill="{CREAM}" stroke="{INK}" stroke-width="6"/>
          <path d="{star_path(540, 760, 120, 52)}" fill="{CREAM}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
          <text x="540" y="920" text-anchor="middle" font-family="Archivo Black" font-size="46" fill="{INK}">TON LOGO</text>
        </g>
      </g>'''
    def blob(i, cx, col, eye_dx, hat):
        return f'''<g id="s4-c{i}">
          <ellipse cx="{cx}" cy="960" rx="120" ry="24" fill="{INK}" opacity="0.18"/>
          <path d="M{cx - 110} 950 C {cx - 130} 700, {cx - 70} 600, {cx} 600 C {cx + 70} 600, {cx + 130} 700, {cx + 110} 950 Z" fill="{col}" stroke="{INK}" stroke-width="8"/>
          <circle cx="{cx - 38 + eye_dx}" cy="720" r="22" fill="#fff" stroke="{INK}" stroke-width="5"/><circle cx="{cx - 34 + eye_dx}" cy="724" r="10" fill="{INK}"/>
          <circle cx="{cx + 38 + eye_dx}" cy="720" r="22" fill="#fff" stroke="{INK}" stroke-width="5"/><circle cx="{cx + 42 + eye_dx}" cy="724" r="10" fill="{INK}"/>
          <path d="M{cx - 30} 800 Q {cx} 830 {cx + 30} 800" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
          {hat}
        </g>'''
    chars = (blob(0, 230, YELLOW, -6, f'<path d="M150 615 L230 470 L310 615 Z" fill="{RED}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
             + blob(1, 540, "#6FC3E8", 0, f'<rect x="470" y="560" width="140" height="50" rx="10" fill="{INK}"/><rect x="500" y="490" width="80" height="80" rx="10" fill="{INK}"/>')
             + blob(2, 850, "#9BD86B", 6, f'<circle cx="850" cy="585" r="34" fill="{ORANGE}" stroke="{INK}" stroke-width="7"/>'))
    html = f'''      <div id="s4-label" class="chip" style="left:0;top:280px;width:1080px;height:96px;text-align:center;background:none;color:{INK};font-size:64px;">
        <span id="s4-lab0">FIGURINE</span><span id="s4-lab1">PORTE-CLÉS</span><span id="s4-lab2">PERSONNAGES</span>
      </div>
      <svg class="{sid}-svg" viewBox="0 0 1080 1920">
        <g id="s4-b0">{fig}</g>
        <g id="s4-b1">{key}</g>
        <g id="s4-b2"><g id="s4-chars">{chars}</g></g>
      </svg>
'''
    css = f"#s4-label span {{ position: absolute; left: 0; width: 1080px; text-align: center; }}"
    B = BAR
    js = f'''
      blurIn(0.15);
      ["#s4-b0", "#s4-b1", "#s4-b2", "#s4-lab0", "#s4-lab1", "#s4-lab2"].forEach((s) => tl.set(s, {{ opacity: 0 }}, 0));
      // beat 1: figurine
      tl.set("#s4-b0, #s4-lab0", {{ opacity: 1 }}, 0.0);
      tl.fromTo("#s4-fig", {{ scale: 1.3, svgOrigin: "540 960" }}, {{ scale: 1, svgOrigin: "540 960", duration: 0.45, ease: "expo.out" }}, 0.0);
      tl.fromTo("#s4-lab0", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.16 }}, 0.05);
      tl.set("#s4-b0, #s4-lab0", {{ opacity: 0 }}, {B:.3f});
      // beat 2: keychain
      tl.set("#s4-b1, #s4-lab1", {{ opacity: 1 }}, {B:.3f});
      tl.fromTo("#s4-key", {{ scale: 1.3, svgOrigin: "540 420" }}, {{ scale: 1, svgOrigin: "540 420", duration: 0.4, ease: "expo.out" }}, {B:.3f});
      tl.fromTo("#s4-tag", {{ rotation: 24, svgOrigin: "540 480" }}, {{ rotation: 0, svgOrigin: "540 480", duration: 1.2, ease: "elastic.out(1, 0.4)" }}, {B:.3f});
      tl.fromTo("#s4-lab1", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.16 }}, {B + 0.05:.3f});
      tl.set("#s4-b1, #s4-lab1", {{ opacity: 0 }}, {2 * B:.3f});
      // beat 3: characters
      tl.set("#s4-b2, #s4-lab2", {{ opacity: 1 }}, {2 * B:.3f});
      [0, 1, 2].forEach((i) => tl.fromTo("#s4-c" + i, {{ y: 260, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.6)" }}, {2 * B:.3f} + i * 0.09));
      tl.fromTo("#s4-lab2", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.16 }}, {2 * B + 0.05:.3f});
      whipOut();
'''
    return scene_file(sid, d, CREAM, CREAM, css, html, js)

# ---------------------------------------------------------------- S5 sketch -> product
def s5(d):
    sid = "s5-ensemble"
    html = f'''      <svg class="{sid}-svg" viewBox="0 0 1080 1920">
        <g id="s5-paper">
          <rect x="70" y="420" width="420" height="520" rx="14" fill="{CREAM}" transform="rotate(-5 280 680)"/>
          {"".join(f'<line x1="110" y1="{y}" x2="450" y2="{y - 30}" stroke="#9BC4E2" stroke-width="3" opacity="0.6"/>' for y in range(520, 920, 50))}
          <path id="s5-sketch" class="dash" d="{star_path(280, 670, 150, 64)}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>
        </g>
        <path id="s5-arrow" class="dash" d="M500 680 C 540 640, 580 640, 610 680" fill="none" stroke="{YELLOW}" stroke-width="12" stroke-linecap="round"/>
        <g id="s5-prod">
          <path d="{star_path(812, 702, 170, 72)}" fill="{ORANGE_D}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
          <path d="{star_path(800, 680, 170, 72)}" fill="{ORANGE}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
          {"".join(f'<line x1="680" y1="{y}" x2="920" y2="{y}" stroke="{INK}" stroke-width="2" opacity="0.15"/>' for y in range(560, 820, 18))}
        </g>
      </svg>
      <div id="s5-chip-a" class="chip" style="left:120px;top:960px;background:{CREAM};color:{INK};font-size:40px;">TON IDÉE</div>
      <div id="s5-chip-b" class="chip" style="left:610px;top:960px;background:{ORANGE};color:{CREAM};font-size:40px;">TON PRODUIT</div>
      <div id="s5-plus" style="position:absolute;left:0;top:290px;width:1080px;text-align:center;font-size:72px;color:{CREAM};"><span id="s5-toi" style="display:inline-block;color:{YELLOW}">TOI</span> <span id="s5-pl" style="display:inline-block">+</span> <span id="s5-nous" style="display:inline-block;color:{ORANGE}">NOUS</span></div>
'''
    js = f'''
      whipIn();
      tl.fromTo("#s5-paper", {{ y: 120, rotation: 6, opacity: 0, svgOrigin: "280 680" }}, {{ y: 0, rotation: 0, opacity: 1, svgOrigin: "280 680", duration: 0.5, ease: "power4.out" }}, 0.2);
      pop("#s5-chip-a", 0.5);
      tl.fromTo("#s5-sketch", {{ strokeDashoffset: 2000 }}, {{ strokeDashoffset: 0, duration: 1.4, ease: "power1.inOut" }}, 0.6);
      tl.fromTo(["#s5-toi", "#s5-pl", "#s5-nous"], {{ opacity: 0, filter: "blur(6px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.13, stagger: 0.12 }}, 1.0);
      tl.fromTo("#s5-arrow", {{ strokeDashoffset: 2000 }}, {{ strokeDashoffset: 0, duration: 0.35, ease: "power2.out" }}, 2.4);
      tl.fromTo("#s5-prod", {{ scale: 0.3, opacity: 0, rotation: -30, svgOrigin: "800 680" }}, {{ scale: 1, opacity: 1, rotation: 0, svgOrigin: "800 680", duration: 0.6, ease: "back.out(1.5)" }}, 2.75);
      pop("#s5-chip-b", 3.0);
      blurOut();
'''
    return scene_file(sid, d, INK, INK, "", html, js)

# ---------------------------------------------------------------- S6 exclusivity
def s6(d, caps):
    sid = "s6-exclu"
    g = {c["text"]: c["start"] - bar(12) for c in caps}
    t_ask, t_conc, t_prod = g["Tu peux nous demander"], g["à un concurrent précis."], g["Tes produits,"]
    html = f'''      <svg class="{sid}-svg" viewBox="0 0 1080 1920">
        <g id="s6-shop">{shop("s6-shop-in", 600, 560, 400, "#5E6068", "EN FACE", body="#C9C9CF")}</g>
        <g id="s6-box">
          <path d="M150 760 L300 690 L450 760 L300 830 Z" fill="#FF9A5C" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
          <path d="M150 760 L300 830 L300 1000 L150 930 Z" fill="{ORANGE}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
          <path d="M450 760 L300 830 L300 1000 L450 930 Z" fill="{ORANGE_D}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
        </g>
        <path id="s6-route" class="dash" d="M440 700 C 500 560, 600 520, 690 560" fill="none" stroke="{CREAM}" stroke-width="10" stroke-linecap="round"/>
        <g id="s6-x"><circle cx="570" cy="580" r="62" fill="{RED}" stroke="{INK}" stroke-width="8"/>
          <path d="M540 550 L600 610 M600 550 L540 610" stroke="{CREAM}" stroke-width="14" stroke-linecap="round"/></g>
        <g id="s6-lock">
          <path id="s6-shackle" d="M262 640 L262 590 A38 38 0 0 1 338 590 L338 640" fill="none" stroke="{YELLOW}" stroke-width="16" stroke-linecap="round"/>
          <rect x="240" y="630" width="120" height="96" rx="16" fill="{YELLOW}" stroke="{INK}" stroke-width="7"/>
          <circle cx="300" cy="672" r="12" fill="{INK}"/><rect x="295" y="676" width="10" height="26" fill="{INK}"/>
        </g>
      </svg>
      <div id="s6-stamp" class="chip" style="left:0;top:290px;width:1080px;text-align:center;background:none;color:{YELLOW};font-size:96px;">EXCLUSIF</div>
      <div id="s6-q" style="position:absolute;left:740px;top:300px;font-size:200px;color:{CREAM};">?</div>
'''
    js = f'''
      blurIn(0.18);
      tl.fromTo("#s6-shop", {{ x: 420, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.5, ease: "power4.out" }}, 0.1);
      tl.fromTo("#s6-q", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)" }}, 0.5);
      tl.to("#s6-q", {{ opacity: 0, scale: 0.6, duration: 0.15, ease: "power2.in" }}, {t_ask - 0.2:.3f});
      tl.fromTo("#s6-box", {{ y: 300, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, {t_ask - 0.1:.3f});
      tl.fromTo("#s6-route", {{ strokeDashoffset: 2000 }}, {{ strokeDashoffset: 0, duration: 0.7, ease: "power2.inOut" }}, {t_ask + 0.6:.3f});
      tl.fromTo("#s6-x", {{ scale: 0, svgOrigin: "570 580" }}, {{ scale: 1, svgOrigin: "570 580", duration: 0.35, ease: "back.out(2.2)" }}, {t_conc:.3f});
      tl.fromTo("#s6-stamp", {{ scale: 2.2, opacity: 0, rotation: -6 }}, {{ scale: 1, opacity: 1, rotation: -3, duration: 0.24, ease: "power4.in" }}, {t_conc + 0.25:.3f});
      tl.fromTo("#s6-shop", {{ filter: "grayscale(0) brightness(1)" }}, {{ filter: "grayscale(1) brightness(0.55)", duration: 0.5, ease: "power2.out" }}, {t_prod:.3f});
      tl.fromTo("#s6-lock", {{ y: -200, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "back.out(1.6)" }}, {t_prod + 0.1:.3f});
      tl.fromTo("#s6-shackle", {{ y: -26 }}, {{ y: 0, duration: 0.14, ease: "power3.in" }}, {t_prod + 0.9:.3f});
      blurOut();
'''
    return scene_file(sid, d, SLATE, SLATE, "", html, js), t_conc + 0.25, t_prod + 0.9

# ---------------------------------------------------------------- S7 easy
def s7(d, caps):
    sid = "s7-facile"
    g = {c["text"]: c["start"] - bar(17) for c in caps}
    t_ok, t_give, t_rest = g["Pas de problème."], g["Tu nous donnes"], g["on s’occupe du reste."]
    html = f'''      <div id="s7-q" style="position:absolute;left:0;top:330px;width:1080px;text-align:center;font-size:520px;line-height:1;color:{INK};">?</div>
      <svg class="{sid}-svg" viewBox="0 0 1080 1920">
        <g id="s7-ok"><circle cx="540" cy="620" r="230" fill="{GREEN}" stroke="{INK}" stroke-width="10"/>
          <path id="s7-tick" class="dash" d="M430 625 L515 705 L665 535" fill="none" stroke="{CREAM}" stroke-width="36" stroke-linecap="round" stroke-linejoin="round"/></g>
        <g id="s7-flow">
          <g id="s7-idea"><path d="M110 520 h300 a30 30 0 0 1 30 30 v170 a30 30 0 0 1 -30 30 h-200 l-60 60 v-60 h-40 a30 30 0 0 1 -30 -30 v-170 a30 30 0 0 1 30 -30 Z" fill="#fff" stroke="{INK}" stroke-width="8"/>
            {bulb("s7-bulb", 260, 630, 0.75)}</g>
          <path id="s7-arrow" class="dash" d="M470 650 L600 650" fill="none" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>
          <path id="s7-arrowhead" d="M580 615 L620 650 L580 685" fill="none" stroke="{INK}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
          <g id="s7-gift">
            <rect x="660" y="560" width="300" height="250" rx="18" fill="{ORANGE}" stroke="{INK}" stroke-width="8"/>
            <rect x="640" y="520" width="340" height="70" rx="14" fill="{ORANGE_D}" stroke="{INK}" stroke-width="8"/>
            <rect x="790" y="520" width="40" height="290" fill="{CREAM}" stroke="{INK}" stroke-width="6"/>
            <g id="s7-check"><circle cx="930" cy="520" r="54" fill="{GREEN}" stroke="{INK}" stroke-width="7"/>
              <path d="M905 522 L925 542 L958 502" fill="none" stroke="{CREAM}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></g>
          </g>
        </g>
      </svg>
'''
    js = f'''
      tl.fromTo(ST, {{ clipPath: "circle(0px at 300px 672px)" }}, {{ clipPath: "circle(2300px at 300px 672px)", duration: 0.35, ease: "power3.in" }}, 0);
      tl.fromTo("#s7-q", {{ rotation: -20, scale: 0.6, opacity: 0 }}, {{ rotation: 0, scale: 1, opacity: 1, duration: 0.6, ease: "back.out(1.7)" }}, 0.2);
      tl.to("#s7-q", {{ scale: 0.4, opacity: 0, filter: "blur(8px)", duration: 0.16, ease: "power3.in" }}, {t_ok - 0.12:.3f});
      tl.fromTo("#s7-ok", {{ scale: 0.4, opacity: 0, svgOrigin: "540 620" }}, {{ scale: 1, opacity: 1, svgOrigin: "540 620", duration: 0.4, ease: "back.out(1.8)" }}, {t_ok:.3f});
      tl.fromTo("#s7-tick", {{ strokeDashoffset: 2000 }}, {{ strokeDashoffset: 1600, duration: 0.01 }}, 0);
      tl.fromTo("#s7-tick", {{ strokeDashoffset: 1600 }}, {{ strokeDashoffset: 1600 - 400, duration: 0.3, ease: "power2.out", immediateRender: false }}, {t_ok + 0.15:.3f});
      tl.to("#s7-ok", {{ scale: 0.5, opacity: 0, filter: "blur(8px)", svgOrigin: "540 620", duration: 0.16, ease: "power3.in" }}, {t_give - 0.16:.3f});
      tl.set("#s7-flow", {{ opacity: 0 }}, 0);
      tl.set("#s7-flow", {{ opacity: 1 }}, {t_give:.3f});
      tl.fromTo("#s7-idea", {{ scale: 0.5, opacity: 0, svgOrigin: "260 640" }}, {{ scale: 1, opacity: 1, svgOrigin: "260 640", duration: 0.45, ease: "back.out(1.7)" }}, {t_give:.3f});
      tl.fromTo("#s7-arrow", {{ strokeDashoffset: 2000 }}, {{ strokeDashoffset: 1870, duration: 0.3, ease: "power2.out" }}, {t_rest - 0.4:.3f});
      tl.fromTo("#s7-arrowhead", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08 }}, {t_rest - 0.15:.3f});
      tl.fromTo("#s7-gift", {{ y: 200, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.5)" }}, {t_rest - 0.1:.3f});
      tl.fromTo("#s7-check", {{ scale: 0, svgOrigin: "930 520" }}, {{ scale: 1, svgOrigin: "930 520", duration: 0.35, ease: "back.out(2.5)" }}, {t_rest + 0.5:.3f});
'''
    return scene_file(sid, d, CREAM, SLATE, "", html, js), t_ok, t_rest + 0.5

# ---------------------------------------------------------------- S8 Christmas
def s8(d):
    sid = "s8-noel"
    def orn(i, cx, len_, col, stripe):
        cy = 200 + len_
        return f'''<g id="s8-o{i}">
          <line x1="{cx}" y1="140" x2="{cx}" y2="{cy - 70}" stroke="{CREAM}" stroke-width="4"/>
          <rect x="{cx - 24}" y="{cy - 92}" width="48" height="30" rx="6" fill="#C9A227" stroke="{INK}" stroke-width="5"/>
          <circle cx="{cx}" cy="{cy}" r="78" fill="{col}" stroke="{INK}" stroke-width="7"/>
          <path d="M{cx - 76} {cy} Q {cx} {cy + 30} {cx + 76} {cy}" fill="none" stroke="{stripe}" stroke-width="12"/>
          {"".join(f'<line x1="{cx - 70}" y1="{yy}" x2="{cx + 70}" y2="{yy}" stroke="{INK}" stroke-width="2" opacity="0.15"/>' for yy in range(cy - 60, cy + 70, 14))}
          <circle cx="{cx - 28}" cy="{cy - 30}" r="14" fill="#fff" opacity="0.7"/>
        </g>'''
    html = f'''      <svg class="{sid}-svg" viewBox="0 0 1080 1920">
        {orn(0, 230, 230, "#F5B83D", RED)}{orn(1, 540, 150, GREEN, CREAM)}{orn(2, 850, 260, CREAM, GREEN)}
        <g id="s8-gift">
          <rect x="360" y="700" width="360" height="300" rx="20" fill="{GREEN}" stroke="{INK}" stroke-width="9"/>
          <rect x="335" y="650" width="410" height="80" rx="16" fill="#17703D" stroke="{INK}" stroke-width="9"/>
          <rect x="520" y="650" width="40" height="350" fill="#F5B83D" stroke="{INK}" stroke-width="6"/>
          <g id="s8-bow"><path d="M540 650 C 470 560, 420 620, 540 650 C 660 620, 610 560, 540 650 Z" fill="#F5B83D" stroke="{INK}" stroke-width="7"/></g>
        </g>
      </svg>
      <div id="s8-tag" class="chip" style="left:0;top:960px;width:1080px;text-align:center;background:none;color:{CREAM};font-size:40px;"><span style="background:{INK};padding:12px 26px;border-radius:999px;">TES CRÉATIONS · TA MARQUE</span></div>
'''
    js = f'''
      [0, 1, 2].forEach((i) => tl.fromTo("#s8-o" + i, {{ y: -560, rotation: [10, -8, 12][i], svgOrigin: [230, 540, 850][i] + " 140" }}, {{ y: 0, rotation: 0, svgOrigin: [230, 540, 850][i] + " 140", duration: 1.1, ease: "elastic.out(1, 0.5)" }}, 0.35 + i * 0.12));
      tl.fromTo("#s8-gift", {{ y: 420, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.55, ease: "back.out(1.4)" }}, 1.4);
      tl.fromTo("#s8-bow", {{ scale: 0, svgOrigin: "540 650" }}, {{ scale: 1, svgOrigin: "540 650", duration: 0.4, ease: "back.out(2.5)" }}, 1.8);
      tl.fromTo("#s8-tag", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.18 }}, 2.2);
      whipOut();
'''
    return scene_file(sid, d, XMAS, CREAM, "", html, js)

# ---------------------------------------------------------------- S9 France
FR = [(2.37, 51.05), (2.9, 50.7), (3.6, 50.5), (4.2, 50.0), (4.85, 50.15), (5.0, 49.8), (5.8, 49.55), (6.4, 49.47),
      (7.0, 49.15), (8.2, 48.97), (7.8, 48.5), (7.55, 47.6), (6.9, 47.4), (6.1, 46.6), (6.0, 46.15), (6.8, 46.0),
      (7.0, 45.3), (6.6, 44.8), (7.0, 44.2), (7.5, 43.8), (6.9, 43.5), (6.2, 43.1), (5.3, 43.2), (4.6, 43.4),
      (3.9, 43.5), (3.1, 43.1), (3.15, 42.45), (2.0, 42.4), (1.0, 42.7), (0.0, 42.75), (-1.0, 43.0), (-1.78, 43.36),
      (-1.45, 43.6), (-1.2, 44.6), (-1.15, 45.6), (-1.6, 46.3), (-2.2, 46.9), (-2.5, 47.3), (-3.3, 47.7), (-4.4, 47.9),
      (-4.75, 48.35), (-4.4, 48.65), (-3.5, 48.8), (-2.6, 48.55), (-1.7, 48.65), (-1.6, 49.2), (-1.85, 49.7),
      (-1.25, 49.7), (-0.6, 49.35), (0.1, 49.45), (0.6, 49.85), (1.4, 50.1), (1.6, 50.6), (1.85, 50.95)]
CITIES = {"Paris": (2.35, 48.86), "Lille": (3.06, 50.63), "Nantes": (-1.55, 47.22), "Bordeaux": (-0.58, 44.84),
          "Toulouse": (1.44, 43.6), "Marseille": (5.37, 43.30), "Lyon": (4.84, 45.76)}
METZ = (6.18, 49.12)
def proj(lon, lat):
    k = math.cos(math.radians(46.5))
    x0, x1 = -4.75 * k, 8.2 * k
    s = 660 / (x1 - x0)
    return 200 + (lon * k - x0) * s, 330 + (51.1 - lat) * s

def s9(d):
    sid = "s9-france"
    poly = " ".join(f"{proj(*p)[0]:.1f},{proj(*p)[1]:.1f}" for p in FR)
    mx, my = proj(*METZ)
    routes, dots = [], []
    for i, (n, c) in enumerate(CITIES.items()):
        cx, cy = proj(*c)
        midx, midy = (mx + cx) / 2, (my + cy) / 2 - 90
        routes.append(f'<path id="s9-r{i}" class="dash s9-route" d="M{mx:.1f} {my:.1f} Q {midx:.1f} {midy:.1f} {cx:.1f} {cy:.1f}" fill="none" stroke="{YELLOW}" stroke-width="6" stroke-linecap="round"/>')
        dots.append(f'<circle id="s9-d{i}" class="s9-dot" cx="{cx:.1f}" cy="{cy:.1f}" r="14" fill="{YELLOW}" stroke="{INK}" stroke-width="5"/>')
    html = f'''      <svg class="{sid}-svg" viewBox="0 0 1080 1920">
        <polygon id="s9-fr" points="{poly}" fill="#1F4A6E" stroke="{CREAM}" stroke-width="8" stroke-linejoin="round"/>
        {"".join(routes)}{"".join(dots)}
        <g id="s9-pin"><path d="M{mx:.1f} {my:.1f} C {mx - 20:.1f} {my - 40:.1f}, {mx - 48:.1f} {my - 60:.1f}, {mx - 48:.1f} {my - 92:.1f} A48 48 0 1 1 {mx + 48:.1f} {my - 92:.1f} C {mx + 48:.1f} {my - 60:.1f}, {mx + 20:.1f} {my - 40:.1f}, {mx:.1f} {my:.1f} Z" fill="{ORANGE}" stroke="{INK}" stroke-width="7"/>
          <circle cx="{mx:.1f}" cy="{my - 92:.1f}" r="18" fill="{CREAM}"/></g>
      </svg>
      <div id="s9-metz" class="chip" style="left:70px;top:285px;background:{ORANGE};color:{CREAM};font-size:32px;border:5px solid {INK};">METZ · EN MAIN PROPRE</div>
      <div id="s9-year" class="chip" style="left:0;top:975px;width:1080px;text-align:center;background:none;color:{CREAM};font-size:44px;"><span style="background:{GREEN};padding:12px 28px;border-radius:999px;">365 JOURS PAR AN</span></div>
'''
    js = f'''
      whipIn();
      tl.fromTo("#s9-fr", {{ opacity: 0, scale: 0.92, svgOrigin: "540 700" }}, {{ opacity: 1, scale: 1, svgOrigin: "540 700", duration: 0.5, ease: "power4.out" }}, 0.05);
      tl.fromTo("#s9-pin", {{ y: -300, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "bounce.out" }}, 0.4);
      pop("#s9-metz", 0.8);
      tl.fromTo(".s9-route", {{ strokeDashoffset: 2000 }}, {{ strokeDashoffset: 1300, duration: 0.6, stagger: 0.12, ease: "power2.out" }}, 2.0);
      tl.fromTo(".s9-dot", {{ scale: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.3, stagger: 0.12, ease: "back.out(2.5)" }}, 2.4);
      tl.fromTo("#s9-year", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.18 }}, 3.3);
      tl.fromTo("#s9-pin", {{ scale: 1, svgOrigin: "{mx:.1f} {my - 92:.1f}" }}, {{ scale: 34, svgOrigin: "{mx:.1f} {my - 92:.1f}", duration: 0.4, ease: "power3.in", immediateRender: false }}, D - 0.4);
      tl.fromTo("#s9-metz, #s9-year", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.15, immediateRender: false }}, D - 0.4);
'''
    return scene_file(sid, d, NAVY, NAVY, "", html, js)

# ---------------------------------------------------------------- S10 DM
def s10(d):
    sid = "s10-dm"
    html = f'''      <div id="s10-card" style="position:absolute;left:110px;top:300px;width:860px;height:760px;border-radius:48px;background:{CREAM};border:8px solid {INK};"></div>
      <div id="s10-head" style="position:absolute;left:150px;top:340px;font-size:44px;color:{INK};">MESSAGE · RenardLab3D</div>
      <div id="s10-typing" style="position:absolute;left:600px;top:520px;width:200px;height:100px;border-radius:50px;background:{ORANGE};display:flex;align-items:center;justify-content:center;gap:16px;">
        <span class="s10-dot" style="width:22px;height:22px;border-radius:50%;background:{CREAM};display:block"></span><span class="s10-dot" style="width:22px;height:22px;border-radius:50%;background:{CREAM};display:block"></span><span class="s10-dot" style="width:22px;height:22px;border-radius:50%;background:{CREAM};display:block"></span>
      </div>
      <div id="s10-msg" style="position:absolute;left:330px;top:500px;width:590px;padding:30px 40px;border-radius:44px 44px 10px 44px;background:{ORANGE};color:{CREAM};font-family:Inter;font-weight:900;font-size:46px;line-height:1.2;">Salut ! J’ai une idée pour ma boutique…</div>
      <div id="s10-input" style="position:absolute;left:150px;top:930px;width:640px;height:90px;border-radius:45px;background:#fff;border:5px solid {INK};"></div>
      <svg class="{sid}-svg" viewBox="0 0 1080 1920">
        <g id="s10-send"><circle cx="870" cy="975" r="56" fill="{INK}"/>
          <path d="M840 975 L905 945 L885 1010 L870 982 Z" fill="{CREAM}"/></g>
      </svg>
'''
    js = f'''
      tl.fromTo("#s10-card", {{ y: 200, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "power4.out" }}, 0.05);
      tl.fromTo("#s10-head, #s10-input, #s10-send", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 0.25);
      tl.fromTo("#s10-typing", {{ opacity: 0, scale: 0.75 }}, {{ opacity: 1, scale: 1, duration: 0.12, ease: "power2.out" }}, 0.5);
      [0, 1, 2].forEach((i) => tl.fromTo(document.querySelectorAll(".s10-dot")[i], {{ y: 0 }}, {{ y: -14, duration: 0.15, yoyo: true, repeat: 3, ease: "sine.inOut" }}, 0.6 + i * 0.1));
      tl.to("#s10-typing", {{ opacity: 0, duration: 0.08 }}, 1.6);
      tl.fromTo("#s10-msg", {{ opacity: 0, scale: 0.75, transformOrigin: "100% 100%" }}, {{ opacity: 1, scale: 1, duration: 0.12, ease: "power2.out" }}, 1.62);
      tl.fromTo("#s10-send", {{ scale: 1, svgOrigin: "870 975" }}, {{ scale: 0.82, svgOrigin: "870 975", duration: 0.08, yoyo: true, repeat: 1 }}, 2.6);
'''
    return scene_file(sid, d, ORANGE, NAVY, "", html, js)

# ---------------------------------------------------------------- S11 share + end card
def s11(d):
    sid = "s11-partage"
    html = f'''      <svg class="{sid}-svg" viewBox="0 0 1080 1920">
        <g id="s11-share">
          {shop("s11-shop", 620, 600, 360, GREEN, "COMMERÇANT")}
          <path id="s11-trail" class="dash" d="M120 900 C 260 600, 420 520, 600 560" fill="none" stroke="{CREAM}" stroke-width="7" stroke-dasharray="18 18" stroke-linecap="round"/>
          <g id="s11-plane"><path d="M-60 0 L60 -40 L20 50 L0 10 Z" fill="{ORANGE}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/></g>
        </g>
      </svg>
      <div id="s11-end" style="position:absolute;left:0;top:0;width:1080px;height:1920px;">
        <div id="s11-word" style="position:absolute;left:0;top:520px;width:1080px;text-align:center;font-size:124px;color:{CREAM};letter-spacing:-0.02em;">RenardLab<span style="color:{ORANGE}">3D</span></div>
        <div id="s11-sub" style="position:absolute;left:0;top:690px;width:1080px;text-align:center;font-family:Inter;font-weight:900;font-size:38px;letter-spacing:0.14em;color:{CREAM};opacity:0.85;">IMPRESSION 3D PERSONNALISÉE</div>
        <div id="s11-loc" style="position:absolute;left:0;top:760px;width:1080px;text-align:center;font-family:Inter;font-weight:700;font-size:36px;color:{CREAM};opacity:0.7;">Metz · livraison partout en France</div>
        <div id="s11-cta" class="chip" style="left:0;top:900px;width:1080px;text-align:center;background:none;color:{INK};font-size:52px;"><span style="background:{ORANGE};padding:18px 44px;border-radius:999px;border:6px solid {CREAM};">ÉCRIS-NOUS EN DM</span></div>
      </div>
'''
    t_end = 2.65
    js = f'''
      tl.fromTo(ST, {{ clipPath: "circle(0px at 870px 975px)" }}, {{ clipPath: "circle(2300px at 870px 975px)", duration: 0.38, ease: "power3.in" }}, 0);
      tl.fromTo("#s11-shop", {{ x: 300, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.5, ease: "power4.out" }}, 0.15);
      tl.fromTo("#s11-trail", {{ strokeDashoffset: 2000 }}, {{ strokeDashoffset: 1300, duration: 1.1, ease: "power1.inOut" }}, 0.5);
      tl.fromTo("#s11-plane", {{ x: 120, y: 900, rotation: -40 }}, {{ x: 610, y: 560, rotation: 10, duration: 1.1, ease: "power1.inOut" }}, 0.5);
      tl.fromTo("#s11-plane", {{ scale: 1, svgOrigin: "0 0" }}, {{ scale: 0, svgOrigin: "0 0", duration: 0.15, ease: "power3.in" }}, 1.6);
      tl.fromTo("#s11-shop", {{ scale: 1, svgOrigin: "800 1000" }}, {{ scale: 1.08, svgOrigin: "800 1000", duration: 0.12, yoyo: true, repeat: 1, ease: "power2.out" }}, 1.65);
      tl.to("#s11-share", {{ opacity: 0, filter: "blur(8px)", duration: 0.18, ease: "power2.in" }}, {t_end - 0.2});
      tl.set("#s11-end", {{ opacity: 0 }}, 0);
      tl.set("#s11-end", {{ opacity: 1 }}, {t_end});
      tl.fromTo("#s11-word", {{ opacity: 0, filter: "blur(10px)", scale: 1.08 }}, {{ opacity: 1, filter: "blur(0px)", scale: 1, duration: 0.2, ease: "power2.out" }}, {t_end});
      tl.fromTo(["#s11-sub", "#s11-loc"], {{ opacity: 0 }}, {{ opacity: (i) => [0.85, 0.7][i], duration: 0.2, stagger: 0.1 }}, {t_end + 0.2});
      tl.fromTo("#s11-cta", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.8)" }}, {t_end + 0.4});
'''
    return scene_file(sid, d, INK, ORANGE, "", html, js), t_end

# ---------------------------------------------------------------- write scenes
dur = {sid: round(bar(e) - bar(s), 3) for sid, s, e, _ in SCENES}
start = {sid: bar(s) for sid, s, e, _ in SCENES}
files = {}
files["s1-hook"] = s1(dur["s1-hook"]); files["s2-reste"] = s2(dur["s2-reste"])
files["s3-marque"], s3_print_end = s3(dur["s3-marque"])
files["s4-produits"] = s4(dur["s4-produits"]); files["s5-ensemble"] = s5(dur["s5-ensemble"])
files["s6-exclu"], s6_stamp, s6_lock = s6(dur["s6-exclu"], CAPTION_TIMES["s6-exclu"])
files["s7-facile"], s7_ok, s7_check = s7(dur["s7-facile"], CAPTION_TIMES["s7-facile"])
files["s8-noel"] = s8(dur["s8-noel"]); files["s9-france"] = s9(dur["s9-france"]); files["s10-dm"] = s10(dur["s10-dm"])
files["s11-partage"], s11_end = s11(dur["s11-partage"])
for sid, txt in files.items():
    open(os.path.join(OUT, "compositions", sid + ".html"), "w").write(txt)

# ---------------------------------------------------------------- captions composition (groups in markup)
groups_html, gi = [], 0
for key, groups in CAPTION_TIMES.items():
    for g in groups:
        words = "".join(
            f'<span class="cw{" emph" if w.lower().strip("?!") in EMPH or w.lower() in EMPH else ""}" data-t="{t}">{w.upper()}</span> '
            for w, t in g["words"])
        groups_html.append(
            f'      <div id="cap-{gi}" class="cap-group clip" data-start="{g["start"]}" data-duration="{round(g["end"] - g["start"], 3)}" data-track-index="0">{words.strip()}</div>')
        gi += 1
captions = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .cap-group {{ position: absolute; left: 90px; top: 1050px; width: 900px; height: 190px; display: flex; flex-wrap: wrap; align-content: center; justify-content: center; column-gap: 0.36em; row-gap: 0.05em; text-align: center; overflow: visible; font-family: "Archivo Black", sans-serif; line-height: 1.05; }}
    .cw {{ display: inline-block; color: #FFFFFF; text-shadow: 0 0 0 {INK}, -5px -5px 0 {INK}, 5px -5px 0 {INK}, -5px 5px 0 {INK}, 5px 5px 0 {INK}, 0 -6px 0 {INK}, 0 6px 0 {INK}, -6px 0 0 {INK}, 6px 0 0 {INK}, 0 12px 22px rgba(0,0,0,0.45); }}
    .cw.emph {{ color: {YELLOW}; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(groups_html)}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      const fit = (window.__hyperframes && window.__hyperframes.fitTextFontSize) || null;
      document.querySelectorAll("#root .cap-group").forEach((g) => {{
        const start = parseFloat(g.dataset.start);
        const text = g.textContent;
        let size = 92;
        if (fit) {{ size = Math.max(58, Math.min(92, fit(text, {{ fontFamily: "Archivo Black", fontWeight: 400, maxWidth: 840, baseFontSize: 92, minFontSize: 58 }}).fontSize)); }}
        g.style.fontSize = size + "px";
        g.querySelectorAll(".cw").forEach((w) => {{
          const t = parseFloat(w.dataset.t);
          const big = w.classList.contains("emph");
          tl.fromTo(w, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.04, ease: "none" }}, t);
          tl.fromTo(w, {{ scale: 0.55, y: 18 }}, {{ scale: big ? 1.12 : 1, y: 0, duration: 0.16, ease: "back.out(2.2)" }}, t);
          if (big) tl.to(w, {{ scale: 1, duration: 0.2, ease: "power2.out" }}, t + 0.16);
        }});
      }});
      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
"""
open(os.path.join(OUT, "compositions", "captions.html"), "w").write(captions)

# ---------------------------------------------------------------- sound placement
LEN = {"whoosh": 0.575, "pop": 0.72, "impact-bass-1": 2.116, "sparkle": 1.802, "click-soft": 0.366}
def sfx(name, picture_t, peak, vol, sid):
    return (sid, name, round(max(0, picture_t - peak + 1 / 30), 3), vol)
P = {"whoosh": 0.162, "pop": 0.12, "impact-bass-1": 0.073, "sparkle": 0.027, "click-soft": 0.073}
reste_t = [w for g in CAPTION_TIMES["s2-reste"] for w in g["words"] if w[0] == "reste."][0][1]
SFX = [
    sfx("whoosh", start["s2-reste"], P["whoosh"], 0.8, "sfx-whip-1"),
    sfx("impact-bass-1", reste_t, P["impact-bass-1"], 0.55, "sfx-reste"),
    sfx("pop", start["s4-produits"], P["pop"], 1.0, "sfx-pop-1"),
    sfx("pop", start["s4-produits"] + BAR, P["pop"], 0.9, "sfx-pop-2"),
    sfx("pop", start["s4-produits"] + 2 * BAR, P["pop"], 1.0, "sfx-pop-3"),
    sfx("whoosh", start["s5-ensemble"], P["whoosh"], 0.65, "sfx-whip-2"),
    sfx("impact-bass-1", start["s6-exclu"] + s6_stamp + 0.24, P["impact-bass-1"], 0.45, "sfx-exclu"),
    sfx("pop", start["s7-facile"] + s7_ok + 0.1, P["pop"], 1.0, "sfx-ok"),
    sfx("whoosh", start["s9-france"], P["whoosh"], 0.75, "sfx-whip-3"),
    sfx("pop", start["s9-france"] + 0.9, P["pop"], 0.9, "sfx-metz"),
    sfx("click-soft", start["s10-dm"] + 2.6, P["click-soft"], 1.0, "sfx-send"),
    sfx("sparkle", start["s11-partage"] + s11_end, P["sparkle"], 0.5, "sfx-end"),
]

# ---------------------------------------------------------------- index.html
hosts = []
for i, (sid, s, e, _) in enumerate(SCENES):
    hosts.append(f'''      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{start[sid]}" data-duration="{dur[sid]}" data-track-index="0" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:1"></div>''')
hosts.append(f'''      <div id="snow" data-composition-id="snow" data-composition-src="compositions/snow.html" data-start="{start["s8-noel"]}" data-duration="{dur["s8-noel"]}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" data-variable-values='{{"density":"dense","speed":"calm"}}' style="z-index:2"></div>''')
hosts.append(f'''      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:3"></div>''')
audio = [f'''      <audio id="music" class="clip" src="assets/bgm/music.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-volume="0.9"></audio>''']
lane_end = []
for sid, name, t, vol in SFX:
    L = LEN[name]
    lane = next((i for i, e in enumerate(lane_end) if e <= t), None)
    if lane is None: lane_end.append(0); lane = len(lane_end) - 1
    lane_end[lane] = t + L
    audio.append(f'''      <audio id="{sid}" class="clip" src="assets/sfx/{name}.mp3" data-start="{t}" data-duration="{L}" data-track-index="{4 + lane}" data-volume="{vol}"></audio>''')

index = f"""<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {INK}; }}
      #root {{ position: relative; width: 1080px; height: 1920px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{chr(10).join(hosts)}
{chr(10).join(audio)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(OUT, "index.html"), "w").write(index)
print("total", TOTAL)
for k, v in CAPTION_TIMES.items():
    for g in v: print(k, g["start"], g["end"], g["text"])
print("sfx", SFX)
