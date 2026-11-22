#!/usr/bin/env python3
"""Jingles v2 (10 s, 120 BPM): banda completa — campanitas, ukulele, pad, bajo con ritmo, batería, arpegio y silbido.
Uso: generar_jingles_v2.py <carpeta de salida>"""
import sys, wave, numpy as np
SR = 44100; OUT = sys.argv[1]; rng = np.random.default_rng(11)
mtof = lambda m: 440.0 * 2 ** ((m - 69) / 12)
BPM = 120; E8 = 60.0 / BPM / 2            # una corchea = 0,25 s ; un compás = 2 s

def put(buf, snd, t, pan=0.0, gain=1.0):
    i = int(t * SR)
    if i >= buf.shape[1] or i < 0: return
    n = min(len(snd), buf.shape[1] - i)
    buf[0, i:i+n] += snd[:n] * gain * (1 - max(0, pan) * .6)
    buf[1, i:i+n] += snd[:n] * gain * (1 + min(0, pan) * .6)

def env(n, a=.003, tau=.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / tau)

def bell(f, dur=1.0):
    t = np.arange(int(dur*SR)) / SR; o = np.zeros_like(t)
    for r, a, tau in [(1, 1, .55), (2.76, .38, .28), (5.4, .16, .14), (8.93, .07, .07)]:
        o += a * np.sin(2*np.pi*f*r*t) * np.exp(-t/tau)
    return o * np.minimum(1, t/.003) * .5

def bass(f, dur=.4):
    t = np.arange(int(dur*SR)) / SR
    return (np.sin(2*np.pi*f*t) + .4*np.sin(2*np.pi*2*f*t) + .15*np.sin(2*np.pi*3*f*t)) * env(len(t), .004, .14) * .9

def ks(f, dur=.6):
    n = int(dur*SR); d = int(SR/f); b = rng.uniform(-1, 1, d); o = np.zeros(n)
    for i in range(n):
        o[i] = b[i % d]; b[i % d] = .4975*(b[i % d] + b[(i+1) % d])
    return o * env(n, .002, .45) * .7

def marimba(f, dur=.3):
    t = np.arange(int(dur*SR)) / SR
    return (np.sin(2*np.pi*f*t) + .25*np.sin(2*np.pi*4*f*t)*np.exp(-t/.03)) * env(len(t), .003, .11) * .6

def pad(freqs, dur):
    t = np.arange(int(dur*SR)) / SR; o = np.zeros_like(t)
    for f in freqs:
        for det in (.997, 1.003):
            for h, a in ((1, 1), (2, .35), (3, .2), (4, .1)):
                o += a * np.sin(2*np.pi*f*det*h*t)
    e = np.minimum(1, t/.08) * np.minimum(1, (dur - t)/.12)
    return o * e * (.9 + .1*np.sin(2*np.pi*4*t)) * .045

def whistle(f, dur=.5):
    t = np.arange(int(dur*SR)) / SR
    ph = 2*np.pi*f*t + 3*np.sin(2*np.pi*5.5*t) * np.minimum(1, t/.15)
    return (np.sin(ph) + .08*np.sin(2*ph)) * np.minimum(1, t/.03) * np.minimum(1, (dur - t)/.08) * .32

def noise_hit(dur, tau, hp=True):
    n = int(dur*SR); x = rng.uniform(-1, 1, n)
    if hp: x = np.diff(x, prepend=0)
    return x * np.exp(-np.arange(n)/SR/tau)

def kick():
    t = np.arange(int(.22*SR)) / SR
    return np.sin(2*np.pi*(52*t + 50*(1 - np.exp(-t*32))/32)) * np.exp(-t/.09)

def snare():
    t = np.arange(int(.2*SR)) / SR
    return (noise_hit(.2, .06)*.7 + np.sin(2*np.pi*190*t)*np.exp(-t/.05)*.5)

def riser(dur):
    n = int(dur*SR); t = np.arange(n)/SR
    x = rng.uniform(-1, 1, n); x = np.convolve(x, np.ones(6)/6, 'same')
    return x * (t/dur)**2 * .5

CH = {'C': (36, [60, 64, 67], [48, 52, 55]), 'G': (31, [59, 62, 67], [43, 47, 50]),
      'Am': (33, [60, 64, 69], [45, 48, 52]), 'F': (29, [60, 65, 69], [41, 45, 48])}
PROG = ['C', 'G', 'Am', 'F']
MEL = [
    [(0,76),(1,76),(2,79),(2.5,81),(3,84),(4,81),(5,79),(6,76),(7,79)],
    [(0,74),(1,74),(2,79),(2.5,83),(3,86),(4,83),(5,81),(6,79),(7,83)],
    [(0,76),(1,76),(2,81),(2.5,84),(3,88),(4,84),(5,83),(6,81),(7,84)],
    [(0,77),(1,77),(2,81),(2.5,84),(3,89),(4,84),(5,81),(6,77),(7,81)],
]

def build(name, lead_extra):
    buf = np.zeros((2, int(10 * SR)))
    for bar, ch in enumerate(PROG):
        t0 = bar * 8 * E8; root, tri, low = CH[ch]
        put(buf, pad([mtof(m) for m in tri], 8*E8 + .1), t0, gain=1.0)
        # bajo con ritmo (corcheas con salto de octava)
        for pos, oct_ in ((0, 0), (1.5, 1), (3, 0), (4, 0), (5.5, 1), (7, 0)):
            put(buf, bass(mtof(root + 12*oct_ + 12)), t0 + pos*E8, gain=.75)
        # batería
        for pos in (0, 2, 4, 6): put(buf, kick(), t0 + pos*E8, gain=.7 if pos in (0, 4) else .35)
        for pos in (2, 6): put(buf, snare(), t0 + pos*E8, gain=.55)
        for pos in range(8):
            put(buf, noise_hit(.045, .013), t0 + pos*E8, pan=.35, gain=.28)
            put(buf, noise_hit(.12, .05), t0 + (pos+.5)*E8, pan=.35, gain=.22)
        # ukulele rasgueado D-DU-UDU
        for pos in (0, 2, 3, 5, 6, 7):
            for k, m in enumerate(tri):
                put(buf, ks(mtof(m)), t0 + pos*E8 + k*.011, pan=-.4, gain=.3)
        # arpegio de marimba en semicorcheas (suave)
        arp = [low[0] + 12, low[1] + 12, low[2] + 12, low[1] + 12]
        for s in range(16): put(buf, marimba(mtof(arp[s % 4])), t0 + s*E8/2, pan=-.15, gain=.17)
        # melodía: campanitas (+ silbido o doblado de octava)
        for pos, m in MEL[bar]:
            put(buf, bell(mtof(m), 1.0), t0 + pos*E8, pan=.2, gain=.6)
            if lead_extra == 'silbido': put(buf, whistle(mtof(m), .38), t0 + pos*E8, pan=.1, gain=.8)
            else: put(buf, bell(mtof(m + 12), .6), t0 + pos*E8, pan=.3, gain=.22)
    # final: crescendo, golpe de platillo y acorde de campanas
    t_end = 4 * 8 * E8
    put(buf, riser(.9), t_end - .9, gain=.8)
    put(buf, noise_hit(1.4, .5), t_end, gain=.5)
    put(buf, kick(), t_end, gain=.9)
    put(buf, pad([mtof(m) for m in (60, 64, 67, 72)], 1.8), t_end, gain=1.4)
    put(buf, bass(mtof(36 + 12)), t_end, gain=.9)
    for m in (72, 76, 79, 84): put(buf, bell(mtof(m), 1.6), t_end, gain=.45)
    for k, m in enumerate((84, 88, 91, 96)): put(buf, bell(mtof(m), 1.4), t_end + .45 + k*.08, pan=.3, gain=.35)
    # eco suave
    for d, g in ((.11, .2), (.19, .12)):
        di = int(d*SR); buf[:, di:] += buf[:, :-di] * g
    f = np.ones(buf.shape[1]); n = int(.5*SR); f[-n:] = np.linspace(1, 0, n); buf *= f
    buf /= np.abs(buf).max() / 0.8
    with wave.open(f'{OUT}/{name}.wav', 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((buf.T*32767).astype('<i2').tobytes())

build('jingle_C_banda_120bpm', 'octava')
build('jingle_D_silbido_120bpm', 'silbido')
print('ok')
