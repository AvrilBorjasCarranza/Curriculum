#!/usr/bin/env python3
"""Edit the owner's recorded voiceover: best take per line, repeats cut, long pauses shortened,
missing pauses added, cuts on the quietest frame with short fades. Writes one WAV per line and a preview."""
import json, sys, os
import numpy as np, soundfile as sf

REC = sys.argv[1]        # folder with take1..4.wav
OUT = sys.argv[2]        # output folder
os.makedirs(OUT, exist_ok=True)
SR = 48000
HOP = int(SR * 0.01)
SIL_DB = -50.0           # below = silence
MAX_PAUSE = 0.30         # longest pause kept inside a line
KEEP_PAUSE = 0.24        # a long pause becomes this
FADE = 0.010

takes = {i: sf.read(f"{REC}/take{i}.wav")[0] for i in range(1, 5)}

def env_db(x):
    n = len(x) // HOP
    r = np.sqrt(np.mean(x[: n * HOP].reshape(n, HOP) ** 2, axis=1)) + 1e-9
    return 20 * np.log10(r)

ENV = {i: env_db(x) for i, x in takes.items()}

def silences(db, min_len=0.08):
    out, s = [], None
    for k, v in enumerate(db):
        if v < SIL_DB and s is None: s = k
        if v >= SIL_DB and s is not None:
            if (k - s) * 0.01 >= min_len: out.append((s * 0.01, k * 0.01))
            s = None
    if s is not None and (len(db) - s) * 0.01 >= min_len: out.append((s * 0.01, len(db) * 0.01))
    return out

def quietest(db, a, b):
    ka, kb = max(0, int(a * 100)), min(len(db) - 1, int(b * 100))
    return (ka + int(np.argmin(db[ka:kb + 1]))) * 0.01

def refine_start(t, a):
    db = ENV[t]
    gaps = [g for g in silences(db) if a - 0.45 <= g[1] <= a + 0.2]
    if gaps:
        g = min(gaps, key=lambda g: abs(g[1] - a))
        return max(g[0], g[1] - 0.04)
    return quietest(db, a - 0.15, a + 0.08)

def refine_end(t, b):
    db = ENV[t]
    gaps = [g for g in silences(db) if b - 0.6 <= g[0] <= b + 0.1]
    if gaps:
        g = min(gaps, key=lambda g: abs(g[0] - b))
        return min(g[1], g[0] + 0.07)
    return quietest(db, b - 0.15, b + 0.08)

def fade(y):
    n = min(int(FADE * SR), len(y) // 4)
    if n > 0:
        y[:n] *= np.linspace(0, 1, n); y[-n:] *= np.linspace(1, 0, n)
    return y

def cut(t, a, b):
    return fade(takes[t][int(a * SR):int(b * SR)].copy())

def tighten(y):
    """Shorten silences longer than MAX_PAUSE inside a line."""
    db = env_db(y); parts, last = [], 0.0
    for s0, s1 in silences(db, MAX_PAUSE):
        if s0 < 0.05 or s1 > len(y) / SR - 0.05: continue
        mid = (s0 + s1) / 2
        parts.append(fade(y[int(last * SR):int((mid - KEEP_PAUSE / 2) * SR)].copy()))
        last = mid + KEEP_PAUSE / 2
    parts.append(fade(y[int(last * SR):].copy()))
    return np.concatenate(parts)

def add_pauses(t, a, b, at, dur=0.2):
    """Line from take t [a,b] with silence inserted at the quietest frame near each time in `at`."""
    pts = [quietest(ENV[t], x - 0.08, x + 0.06) for x in at]
    edges = [a] + pts + [b]; out = []
    for i in range(len(edges) - 1):
        out.append(cut(t, edges[i], edges[i + 1]))
        if i < len(edges) - 2: out.append(np.zeros(int(dur * SR)))
    return np.concatenate(out)

# line: (take, first word start, start of the word after the line, [times to add a pause before])
LINES = {
    "s1": (3, 6.0, 10.4, []),
    "s2": (4, 4.8, 7.5, []),
    "s3": (3, 15.0, 20.0, []),
    "s4a": (3, 20.0, 21.4, []),
    "s4b": (3, 21.4, 22.8, []),
    "s4c": (3, 22.8, 24.2, []),
    "s5": (3, 24.2, 28.0, []),
    "s6": (2, 24.5, 32.0, []),
    "s7": (3, 38.0, 47.0, [42.1]),
    "s8": (3, 47.0, 51.0, []),
    "s9": (1, 75.6, 79.7, [77.1, 78.9]),
    "s10": (2, 52.9, 56.4, []),
    "s11": (2, 56.4, 61.5, []),
}
START_FIX = {"s2": 4.69}   # take 4: the tail of "idées" ends at 4.68 s, "Si" starts at 4.71 s
report = {}
for k, (t, a, b, extra) in LINES.items():
    a2, b2 = refine_start(t, a), refine_end(t, b)
    a2 = START_FIX.get(k, a2)
    y = add_pauses(t, a2, b2, extra) if extra else cut(t, a2, b2)
    y = tighten(y)
    sf.write(f"{OUT}/{k}.wav", y.astype(np.float32), SR)
    report[k] = {"take": t, "from": round(a2, 2), "to": round(b2, 2), "dur": round(len(y) / SR, 2)}

GAP = {"s1": 0.5, "s4a": 0.32, "s4b": 0.32, "s4c": 0.45}
order = ["s1", "s2", "s3", "s4a", "s4b", "s4c", "s5", "s6", "s7", "s8", "s9", "s10", "s11"]
prev = []
for k in order:
    prev.append(sf.read(f"{OUT}/{k}.wav")[0]); prev.append(np.zeros(int(GAP.get(k, 0.4) * SR)))
sf.write(f"{OUT}/preview_raw.wav", np.concatenate(prev).astype(np.float32), SR)
json.dump(report, open(f"{OUT}/edit_report.json", "w"), indent=1)
for k, v in report.items(): print(k, v)
