#!/usr/bin/env python3
"""Música «de burbujas que explotan» (10 s): sin agudos. Percusión hecha de pops, blops graves que suben, marimba/kalimba cálidas y bajo suave.
Uso: generar_pops.py <carpeta de salida>"""
import sys, wave, numpy as np
SR = 44100; OUT = sys.argv[1]; rng = np.random.default_rng(9)
mtof = lambda m: 440.0 * 2 ** ((m - 69) / 12)

def put(buf, snd, t, pan=0.0, gain=1.0):
    i = int(t * SR)
    if i < 0 or i >= buf.shape[1]: return
    n = min(len(snd), buf.shape[1] - i)
    buf[0, i:i+n] += snd[:n] * gain * (1 - max(0, pan) * .6); buf[1, i:i+n] += snd[:n] * gain * (1 + min(0, pan) * .6)

def lowpass(x, fc):
    a = np.exp(-2*np.pi*fc/SR); y = np.zeros_like(x); s = 0.0
    for i in range(len(x)): s = (1 - a) * x[i] + a * s; y[i] = s
    return y

def pop(f0=620, f1=170, dur=.11, tau=.014, decay=.028, click=.35):
    """Pop de burbuja: golpe de seno que cae de tono + chasquido corto filtrado."""
    t = np.arange(int(dur*SR)) / SR
    fr = f1 + (f0 - f1) * np.exp(-t / tau); ph = 2*np.pi*np.cumsum(fr)/SR
    n = lowpass(rng.uniform(-1, 1, len(t)), 2200) * np.exp(-t/.006) * click
    return (np.sin(ph) * np.exp(-t/decay) + n) * np.minimum(1, t/.0008)

def bloop(f_end, dur=.16, f_start=0.55):
    """Burbuja que sube (grave, redonda)."""
    t = np.arange(int(dur*SR)) / SR
    fr = f_end * (f_start + (1 - f_start) * (1 - np.exp(-t / .03))); ph = 2*np.pi*np.cumsum(fr)/SR
    return np.sin(ph) * np.exp(-t/.07) * np.minimum(1, t/.004) * .8

def marimba(f, dur=.45):
    t = np.arange(int(dur*SR)) / SR
    return (np.sin(2*np.pi*f*t) + .2*np.sin(2*np.pi*4*f*t)*np.exp(-t/.03)) * np.exp(-t/.16) * np.minimum(1, t/.003) * .8

def kalimba(f, dur=.6):
    t = np.arange(int(dur*SR)) / SR
    return (np.sin(2*np.pi*f*t) + .12*np.sin(2*np.pi*5.4*f*t)*np.exp(-t/.02)) * np.exp(-t/.28) * np.minimum(1, t/.002) * .75

def bass(f, dur=.4):
    t = np.arange(int(dur*SR)) / SR
    return (np.sin(2*np.pi*f*t) + .2*np.sin(2*np.pi*2*f*t)) * np.exp(-t/.2) * np.minimum(1, t/.005) * .95

def pad(freqs, dur):
    t = np.arange(int(dur*SR)) / SR; o = np.zeros_like(t)
    for f in freqs:
        for det in (.998, 1.002): o += np.sin(2*np.pi*f*det*t) + .12*np.sin(2*np.pi*2*f*det*t)
    return o * np.minimum(1, t/.12) * np.minimum(1, (dur-t)/.18) * .05

def uke(f, dur=.3):
    n = int(dur*SR); d = int(SR/f); b = rng.uniform(-1, 1, d); o = np.zeros(n)
    for i in range(n):
        o[i] = b[i % d]; b[i % d] = .497*(b[i % d] + b[(i+1) % d])
    return lowpass(o, 2600) * np.exp(-np.arange(n)/SR/.18) * np.minimum(1, np.arange(n)/(.002*SR)) * .8

CH = {'C': (36, [55, 59, 62]), 'G': (31, [55, 59, 62]), 'Am': (33, [57, 60, 64]), 'F': (29, [57, 60, 65])}   # raíz del bajo y acorde (registro medio)
PROG = ['C', 'G', 'Am', 'F']
MEL = [[(0,67),(1,71),(2,74),(3,71),(4,69),(5,71),(6,67),(7,64)],
       [(0,66),(1,69),(2,71),(3,69),(4,67),(5,69),(6,74),(7,71)],
       [(0,69),(1,72),(2,76),(3,72),(4,71),(5,72),(6,69),(7,67)],
       [(0,72),(1,69),(2,65),(3,69),(4,72),(5,76),(6,74),(7,72)]]

def build(name, bpm, voice, o):
    E = 60.0 / bpm / 2
    buf = np.zeros((2, int(10 * SR)))
    for bar, ch in enumerate(PROG):
        t0 = bar * 8 * E; root, tri = CH[ch]
        put(buf, pad([mtof(m) for m in tri], 8*E + .1), t0, gain=o['pad'])
        for pos in (0, 3, 4, 7): put(buf, bass(mtof(root + 12)), t0 + pos*E, gain=o['bass'])
        for pos in (0, 4): put(buf, pop(260, 70, .16, .02, .06, .1), t0 + pos*E, gain=.8 * o['kick'])             # bombo = pop grave
        for pos in (2, 6): put(buf, pop(900, 260, .12, .012, .03, .5), t0 + pos*E, pan=.1, gain=o['snare'])         # caja = pop medio
        for pos in range(8):                                                                                       # pops pequeños en las corcheas
            f0 = 1100 + 250 * ((pos * 5 + bar) % 4)
            put(buf, pop(f0, f0 * .32, .07, .009, .018, .3), t0 + (pos + .5)*E, pan=.4 if pos % 2 else -.4, gain=o['tick'])
        for pos, m in MEL[bar]:
            f = mtof(m)
            put(buf, (marimba(f) if voice == 'marimba' else kalimba(f)), t0 + pos*E, pan=.15, gain=o['mel'])
        if o['uke']:
            for pos in (1, 3, 5, 7):
                for k, m in enumerate(tri): put(buf, uke(mtof(m)), t0 + pos*E + k*.012, pan=-.3, gain=o['uke'])
        if o['bloops']:                                                                                            # burbujas graves que suben antes de cada pop
            for pos, m in ((1.5, 60), (3.5, 64), (5.5, 62), (7.5, 67)):
                put(buf, bloop(mtof(m)), t0 + pos*E, pan=-.35 if pos % 2 else .35, gain=o['bloops'])
    te = 4 * 8 * E
    for k in range(6): put(buf, bloop(mtof(55 + 2*k), .13), te - 1.0 + k*.15, pan=-.5 + .2*k, gain=.7)           # subida de burbujas
    for k in range(7): put(buf, pop(900 - 60*k, 250, .1, .012, .03, .5), te + k*.07, pan=-.6 + .2*k, gain=.8)      # estallido de varias burbujas
    for m in (55, 59, 62, 67): put(buf, kalimba(mtof(m), 1.4), te + .05, gain=.7)
    put(buf, bass(mtof(48)), te, gain=1.0)
    for d, g in ((.12, .2), (.21, .12)):
        di = int(d*SR); buf[:, di:] += buf[:, :-di] * g
    f = np.ones(buf.shape[1]); n = int(.5*SR); f[-n:] = np.linspace(1, 0, n); buf *= f
    buf[0] = lowpass(buf[0], 3500); buf[1] = lowpass(buf[1], 3500)                                                  # sin agudos
    buf /= np.abs(buf).max() / 0.8
    with wave.open(f'{OUT}/{name}.wav', 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((buf.T*32767).astype('<i2').tobytes())

build('jingle_H1_pops_marimba_104bpm', 104, 'marimba', dict(pad=.9, bass=.7, kick=1.0, snare=.8, tick=.28, mel=.6, uke=0, bloops=.45))
build('jingle_H2_pops_kalimba_100bpm', 100, 'kalimba', dict(pad=.8, bass=.65, kick=.9, snare=.7, tick=.35, mel=.65, uke=0, bloops=.6))
build('jingle_H3_pops_ukelele_108bpm', 108, 'marimba', dict(pad=.7, bass=.75, kick=1.0, snare=.85, tick=.3, mel=.5, uke=.32, bloops=.4))
print('ok')
