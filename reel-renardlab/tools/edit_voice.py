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

def remove_breaths(y, quiet_db=-33.0, min_len=0.0):
    """Blocks of sound far below the voice (breaths, sighs, whispered counting) become silence."""
    db = env_db(y); on = db > SIL_DB; k = 0; n = len(on); removed = []
    while k < n:
        if on[k]:
            j = k
            while j < n and (on[j] or on[j:j + 8].any()): j += 1
            if db[k:j].max() < quiet_db and (j - k) * 0.01 >= min_len:
                y[k * HOP:j * HOP] = 0.0; removed.append((round(k * 0.01, 2), round(j * 0.01, 2)))
            k = j
        else:
            k += 1
    return y, removed

def trim_edges(y, core_db=-33.0, lead=0.25, tail=0.40):
    """Start just before the first voiced sound, end just after the last one."""
    db = env_db(y); core = np.where(db > core_db)[0]
    if len(core) == 0: return y
    a = core[0]; b = core[-1]
    k = a
    while k > 0 and db[k - 1] > SIL_DB and (a - k) < lead * 100: k -= 1
    j = b
    while j < len(db) - 1 and db[j + 1] > SIL_DB and (j - b) < tail * 100: j += 1
    s0 = max(0, (k - 3) * HOP); s1 = min(len(y), (j + 6) * HOP)
    return fade(y[s0:s1].copy())

def add_pauses(t, a, b, at, dur=0.2):
    """Line from take t [a,b] with silence inserted at the quietest frame near each time in `at`."""
    pts = [quietest(ENV[t], x - 0.08, x + 0.06) for x in at]
    edges = [a] + pts + [b]; out = []
    for i in range(len(edges) - 1):
        out.append(cut(t, edges[i], edges[i + 1]))
        if i < len(edges) - 2: out.append(np.zeros(int(dur * SR)))
    return np.concatenate(out)

# line: (take, first word start, start of the word after the line, [times to add a pause before])
# word times from faster-whisper (word_timestamps) on each take, checked against the energy envelope
LINES = {
    "s1": (3, 8.42, 10.66, []),
    "s2": (4, 6.00, 8.02, []),
    "s3": (3, 15.18, 20.48, []),
    "s4a": (3, 20.48, 22.04, []),
    "s4b": (3, 22.04, 23.36, []),
    "s4c": (3, 23.36, 24.60, []),
    "s5": (3, 24.50, 27.40, []),
    "s6": (2, 24.84, 32.24, []),
    "s7": (3, 38.64, 47.02, []),
    "s8": (3, 47.02, 51.15, []),
    "s9": (1, 75.96, 79.76, [77.10, 78.54]),
    "s10": (1, 79.76, 81.80, []),
    "s11": (2, 57.30, 60.70, []),
}
START_FIX = {}
report = {}
for k, (t, a, b, extra) in LINES.items():
    a2, b2 = refine_start(t, a), refine_end(t, b)
    a2 = START_FIX.get(k, a2)
    y = add_pauses(t, a2, b2, extra) if extra else cut(t, a2, b2)
    y, br = remove_breaths(y)
    y = trim_edges(tighten(y))
    sf.write(f"{OUT}/{k}.wav", y.astype(np.float32), SR)
    report[k] = {"take": t, "from": round(a2, 2), "to": round(b2, 2), "dur": round(len(y) / SR, 2), "breaths_removed": br}

GAP = {"s1": 0.5, "s4a": 0.32, "s4b": 0.32, "s4c": 0.45}
order = ["s1", "s2", "s3", "s4a", "s4b", "s4c", "s5", "s6", "s7", "s8", "s9", "s10", "s11"]
prev = []
for k in order:
    prev.append(sf.read(f"{OUT}/{k}.wav")[0]); prev.append(np.zeros(int(GAP.get(k, 0.4) * SR)))
sf.write(f"{OUT}/preview_raw.wav", np.concatenate(prev).astype(np.float32), SR)
json.dump(report, open(f"{OUT}/edit_report.json", "w"), indent=1)
for k, v in report.items(): print(k, v)
