#!/usr/bin/env python3
"""Jingles «de burbuja» (10 s): blops de burbuja con glissando, marimba y celesta, pizzicato, bajo suave y pops rítmicos.
Uso: generar_burbujas.py <carpeta de salida>"""
import sys, wave, numpy as np
SR = 44100; OUT = sys.argv[1]; rng = np.random.default_rng(5)
mtof = lambda m: 440.0 * 2 ** ((m - 69) / 12)

def put(buf, snd, t, pan=0.0, gain=1.0):
    i = int(t * SR)
    if i < 0 or i >= buf.shape[1]: return
    n = min(len(snd), buf.shape[1] - i)
    buf[0, i:i+n] += snd[:n] * gain * (1 - max(0, pan) * .6); buf[1, i:i+n] += snd[:n] * gain * (1 + min(0, pan) * .6)

def blop(f, dur=.18, up=1.9):
    """Burbuja: seno que sube rápido de tono y se apaga (como una gota o burbuja)."""
    t = np.arange(int(dur*SR)) / SR
    fr = f * (1 + (up - 1) * (1 - np.exp(-t / .035)))
    ph = 2*np.pi*np.cumsum(fr)/SR
    return np.sin(ph) * np.exp(-t/.06) * np.minimum(1, t/.002) * .9

def bubble_pop(dur=.06):
    n = int(dur*SR); t = np.arange(n)/SR
    x = rng.uniform(-1, 1, n); x = np.convolve(x, np.ones(3)/3, 'same')
    return (x * np.exp(-t/.012) * .5 + np.sin(2*np.pi*(900 + 1800*np.exp(-t*60))*t) * np.exp(-t/.02) * .5)

def marimba(f, dur=.3):
    t = np.arange(int(dur*SR)) / SR
    return (np.sin(2*np.pi*f*t) + .25*np.sin(2*np.pi*4*f*t)*np.exp(-t/.03)) * np.exp(-t/.11) * np.minimum(1, t/.003) * .6

def celesta(f, dur=.9):
    t = np.arange(int(dur*SR)) / SR
    return (np.sin(2*np.pi*f*t) + .3*np.sin(2*np.pi*3*f*t)*np.exp(-t/.1) + .12*np.sin(2*np.pi*5.1*f*t)*np.exp(-t/.05)) * np.exp(-t/.45) * np.minimum(1, t/.002) * .5

def pluck(f, dur=.25):
    t = np.arange(int(dur*SR)) / SR
    return (np.sin(2*np.pi*f*t) + .3*np.sin(2*np.pi*2*f*t)) * np.exp(-t/.07) * np.minimum(1, t/.002) * .7

def bass(f, dur=.35):
    t = np.arange(int(dur*SR)) / SR
    return (np.sin(2*np.pi*f*t) + .25*np.sin(2*np.pi*2*f*t)) * np.exp(-t/.17) * np.minimum(1, t/.004) * .9

def softkick():
    t = np.arange(int(.18*SR)) / SR
    return np.sin(2*np.pi*(50*t + 40*(1-np.exp(-t*30))/30)) * np.exp(-t/.07) * .7

def snap(dur=.07):
    n = int(dur*SR); x = rng.uniform(-1, 1, n); return np.diff(x, prepend=0) * np.exp(-np.arange(n)/SR/.016) * .35

def pad(freqs, dur):
    t = np.arange(int(dur*SR)) / SR; o = np.zeros_like(t)
    for f in freqs:
        for det in (.998, 1.002): o += np.sin(2*np.pi*f*det*t) + .15*np.sin(2*np.pi*2*f*det*t)
    return o * np.minimum(1, t/.1) * np.minimum(1, (dur-t)/.15) * .05

BPM = 108; E = 60.0 / BPM / 2          # corchea ≈ .278 s ; compás ≈ 2.22 s
CH = {'C': (48, [60, 64, 67]), 'G': (43, [59, 62, 67]), 'Am': (45, [60, 64, 69]), 'F': (41, [60, 65, 69])}
PROG = ['C', 'G', 'Am', 'F']
MEL = [[(0,79),(1,83),(2,86),(3,83),(4,81),(5,83),(6,79),(7,76)],
       [(0,78),(1,81),(2,83),(3,81),(4,79),(5,81),(6,86),(7,83)],
       [(0,81),(1,84),(2,88),(3,84),(4,83),(5,84),(6,81),(7,79)],
       [(0,84),(1,81),(2,77),(3,81),(4,84),(5,88),(6,86),(7,84)]]

def build(name, rich):
    buf = np.zeros((2, int(10 * SR)))
    for bar, ch in enumerate(PROG):
        t0 = bar * 8 * E; root, tri = CH[ch]
        put(buf, pad([mtof(m) for m in tri], 8*E + .1), t0)
        for pos in (0, 3, 4, 7):
            put(buf, bass(mtof(root)), t0 + pos*E, gain=.7)
        for pos in (0, 4): put(buf, softkick(), t0 + pos*E, gain=.55)
        for pos in (2, 6): put(buf, snap(), t0 + pos*E, gain=.7)
        for pos in range(8):                                    # pops de burbuja como «hi-hat»
            put(buf, bubble_pop(), t0 + (pos + .5)*E, pan=.4 if pos % 2 else -.4, gain=.45 if rich else .3)
        for pos in (1, 3, 5, 7):
            for k, m in enumerate(tri): put(buf, pluck(mtof(m + 12)), t0 + pos*E + k*.008, pan=-.3, gain=.22)
        for pos, m in MEL[bar]:
            put(buf, marimba(mtof(m - 12)), t0 + pos*E, pan=-.1, gain=.55)
            put(buf, celesta(mtof(m)), t0 + pos*E, pan=.2, gain=.45)
        if rich:                                                # blops de burbuja subiendo en las notas largas
            for pos, m in ((1, 88), (3, 91), (5, 93), (7, 96)):
                put(buf, blop(mtof(m - 12), .2, 1.9), t0 + (pos + .5)*E, pan=.45 if pos % 4 == 1 else -.45, gain=.5)
    te = 4 * 8 * E
    for k in range(6): put(buf, blop(mtof(72 + 2*k), .15, 1.8), te - 1.0 + k*.14, pan=-.5 + .2*k, gain=.55)   # subida de burbujas
    for m in (72, 76, 79, 84): put(buf, celesta(mtof(m), 1.6), te, gain=.55)
    put(buf, bass(mtof(36)), te, gain=.9); put(buf, softkick(), te, gain=.8)
    for k, m in enumerate((88, 91, 96, 100)): put(buf, celesta(mtof(m), 1.2), te + .35 + k*.09, pan=.3, gain=.35)
    for d, g in ((.13, .22), (.23, .14), (.37, .08)):
        di = int(d*SR); buf[:, di:] += buf[:, :-di] * g
    f = np.ones(buf.shape[1]); n = int(.5*SR); f[-n:] = np.linspace(1, 0, n); buf *= f
    buf /= np.abs(buf).max() / 0.8
    with wave.open(f'{OUT}/{name}.wav', 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((buf.T*32767).astype('<i2').tobytes())

build('jingle_E_burbujas_108bpm', False)
build('jingle_F_burbujas_blops_108bpm', True)
print('ok')
