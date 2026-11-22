#!/usr/bin/env python3
"""Limpia las capas con sombra renderizadas en Blender: quita el velo casi invisible del 'shadow catcher'
y desvanece los bordes del rectángulo para que no se vea el corte. Uso: pulir_capas.py <carpeta con capa_*.png>"""
import sys, glob, numpy as np
from PIL import Image
for f in sorted(glob.glob(sys.argv[1] + '/capa_*.png')):
    im = np.array(Image.open(f).convert('RGBA')).astype(float); a = im[..., 3] / 255
    a = np.clip((a - 0.035) / 0.965, 0, 1)
    h, w = a.shape; fade = 14
    ey = np.minimum(np.arange(h), np.arange(h)[::-1]); ex = np.minimum(np.arange(w), np.arange(w)[::-1])
    m = np.clip(np.minimum(ey[:, None], ex[None, :]) / fade, 0, 1)
    a = a * m
    im[..., 3] = a * 255
    Image.fromarray(im.astype(np.uint8), 'RGBA').save(f); print('pulida', f)
