#!/usr/bin/env python3
"""Dos jingles alegres de 10 s hechos en código (numpy): campanitas «tin tin tirin». Uso: generar_jingles.py <carpeta de salida>"""
import sys, wave, numpy as np
SR = 44100
OUT = sys.argv[1]
rng = np.random.default_rng(3)
mtof = lambda m: 440.0 * 2 ** ((m - 69) / 12)

def mix(buf, snd, t, pan=0.0, gain=1.0):
    i = int(t * SR)
    if i >= buf.shape[1]: return
    n = min(len(snd), buf.shape[1] - i)
    l, r = (1 - pan) / 2 + 0.5 * (1 - abs(pan)), (1 + pan) / 2 + 0.5 * (1 - abs(pan))
    buf[0, i:i + n] += snd[:n] * gain * min(1, 1 - pan * 0.5)
    buf[1, i:i + n] += snd[:n] * gain * min(1, 1 + pan * 0.5)

def bell(f, dur=1.0):
    t = np.arange(int(dur * SR)) / SR
    out = np.zeros_like(t)
    for ratio, amp, tau in [(1, 1.0, .55), (2.76, .38, .28), (5.4, .16, .14), (8.93, .07, .07)]:
        out += amp * np.sin(2 * np.pi * f * ratio * t) * np.exp(-t / tau)
    out *= np.minimum(1, t / 0.003)
    return out * 0.5

def pluck_bass(f, dur=.5):
    t = np.arange(int(dur * SR)) / SR
    return (np.sin(2*np.pi*f*t) + .35*np.sin(2*np.pi*2*f*t)) * np.exp(-t/.16) * np.minimum(1, t/.004) * .9

def marimba(f, dur=.35):
    t = np.arange(int(dur * SR)) / SR
    return (np.sin(2*np.pi*f*t) + .25*np.sin(2*np.pi*4*f*t)*np.exp(-t/.03)) * np.exp(-t/.12) * np.minimum(1, t/.003) * .6

def ks_pluck(f, dur=.6):
    n = int(dur * SR); d = int(SR / f)
    buf = rng.uniform(-1, 1, d); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % d]
        buf[i % d] = 0.4975 * (buf[i % d] + buf[(i + 1) % d])
    return out * np.minimum(1, np.arange(n)/(.002*SR)) * np.exp(-np.arange(n)/SR/.5) * .7

def shaker(dur=.06):
    n = int(dur*SR); x = rng.uniform(-1, 1, n); x = np.diff(x, prepend=0)
    return x * np.exp(-np.arange(n)/SR/.018) * .3

def kick(dur=.22):
    t = np.arange(int(dur*SR))/SR
    return np.sin(2*np.pi*(55*t + 45*(1-np.exp(-t*30))/30)) * np.exp(-t/.09) * .8

def clap(dur=.12):
    n = int(dur*SR); x = rng.uniform(-1, 1, n)
    return np.diff(x, prepend=0) * np.exp(-np.arange(n)/SR/.035) * .35

CH = {'C': (48, [60, 64, 67]), 'G': (43, [59, 62, 67]), 'Am': (45, [60, 64, 69]), 'F': (41, [60, 65, 69])}
PROG = ['C', 'G', 'Am', 'F', 'C']

def render(name, bpm, melody, strum_ks, bell_oct=0):
    eighth = 60.0 / bpm / 2
    buf = np.zeros((2, int(10.0 * SR)))
    for bar, ch in enumerate(PROG):
        t0 = bar * 8 * eighth
        root, tri = CH[ch]
        for pos in (0, 4, 6) if bar < 4 else (0,):
            mix(buf, pluck_bass(mtof(root), .5), t0 + pos * eighth, gain=.7)
        for pos in (0, 4):
            mix(buf, kick(), t0 + pos * eighth, gain=.55 if bar < 4 else .7)
        for pos in (2, 6):
            mix(buf, clap(), t0 + pos * eighth, gain=.5)
        for pos in range(8):
            mix(buf, shaker(), t0 + (pos + .5) * eighth if pos % 2 == 0 else t0 + pos * eighth, pan=.3 if pos % 2 else -.3, gain=.6)
        if bar < 4:
            for pos in (1, 3, 5, 7):
                if strum_ks:
                    for k, m in enumerate(tri):
                        mix(buf, ks_pluck(mtof(m)), t0 + pos * eighth + k * .012, pan=-.25, gain=.32)
                else:
                    for m in tri:
                        mix(buf, marimba(mtof(m)), t0 + pos * eighth, pan=-.25, gain=.4)
    # melodía de campanitas
    for bar, notes in enumerate(melody):
        t0 = bar * 8 * eighth
        for pos, m in notes:
            mix(buf, bell(mtof(m + 12 * bell_oct), 1.0), t0 + pos * eighth, pan=.25, gain=.55)
    # final: acorde de cierre y destello
    t_end = 4 * 8 * eighth
    for m in (72, 76, 79, 84):
        mix(buf, bell(mtof(m), 1.6), t_end, gain=.45)
    for k, m in enumerate((84, 88, 91, 96)):
        mix(buf, bell(mtof(m), 1.4), t_end + .5 + k * .08, pan=.3, gain=.35)
    # reverb corta (eco suave)
    for d, g in ((.11, .22), (.19, .14)):
        di = int(d * SR); buf[:, di:] += buf[:, :-di] * g
    fade = np.ones(buf.shape[1]); n = int(.4 * SR); fade[-n:] = np.linspace(1, 0, n)
    buf *= fade
    buf /= max(1e-9, np.abs(buf).max()) / 0.8
    pcm = (buf.T * 32767).astype('<i2')
    with wave.open(f'{OUT}/{name}.wav', 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

mel_a = [
    [(0,76),(1,76),(2,79),(3,79),(4,81),(5,79),(6,76)],
    [(0,74),(1,74),(2,79),(3,79),(4,83),(5,81),(6,79)],
    [(0,76),(1,76),(2,81),(3,81),(4,84),(5,83),(6,81)],
    [(0,77),(1,77),(2,81),(3,81),(4,84),(5,81),(6,77)],
]
mel_b = [
    [(0,79),(.5,81),(1,84),(2,79),(2.5,81),(3,84),(4,86),(5,84),(6,81)],
    [(0,79),(.5,83),(1,86),(2,79),(2.5,83),(3,86),(4,88),(5,86),(6,83)],
    [(0,81),(.5,84),(1,88),(2,81),(2.5,84),(3,88),(4,91),(5,88),(6,84)],
    [(0,81),(.5,84),(1,89),(2,81),(2.5,84),(3,89),(4,88),(5,84),(6,81)],
]
render('jingle_A_campanitas_126bpm', 126, mel_a, strum_ks=False)
render('jingle_B_ukulele_132bpm', 132, mel_b, strum_ks=True)
print('ok')
