#!/usr/bin/env python3
"""[VARIANTE SERIE] Pulpo real (STL de Avril) dentro de la playa 3D: giro rápido→lento, caída, aplastamiento y rebote con sombra real.
Uso: python anim_pulpo.py <salida> [--preview] [--frame T] [--body #8363D8] [--exposure 0] """
import sys, os, math, json
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'escena_playa.py')).read()
ARGS = sys.argv[:]
OUTD = ARGS[1]; PREV = '--preview' in ARGS
def arg(n, d=None): return ARGS[ARGS.index(n) + 1] if n in ARGS else d
BODY = arg('--body', '#7051C4'); ONE = arg('--frame'); EXPO = float(arg('--exposure', '0'))
sys.argv = ['x', '/tmp/claude-0/escena_tmp', '--only', 'none'] + (['--preview'] if PREV else [])
exec(compile(SRC, 'escena_playa', 'exec'))
import numpy as np
os.makedirs(OUTD, exist_ok=True)

# ---- escena solo para el pulpo: sombra real sobre la arena, sin las siluetas
vis([], True)
for _o in bpy.data.objects:
    if _o.name.startswith(('s1', 's2', 's3', 's4', 's5')): _o.hide_render = True
proxy.hide_render = True
sun_d.angle = math.radians(22)

# ---- cámara de vídeo: 1080x1920, el «pan» del vídeo = shift vertical del sensor
HF = 1920; RES2 = 0.5 if PREV else 1.0
scene.render.resolution_x = int(1080 * RES2); scene.render.resolution_y = int(HF * RES2); scene.render.resolution_percentage = 100
cam_d.sensor_height = 36.0 * HF / 2700.0
scene.render.film_transparent = True; scene.render.image_settings.color_mode = 'RGBA'
scene.cycles.samples = 24 if PREV else 40
scene.view_settings.exposure = EXPO
# solo se renderiza la zona donde ocurre la acción (el resto queda transparente): ahorra ~45 % de tiempo
scene.render.use_border = True; scene.render.use_crop_to_border = False
scene.render.border_min_x, scene.render.border_max_x, scene.render.border_min_y, scene.render.border_max_y = 0.03, 0.98, 0.0, 0.42
def set_pan(py): cam_d.shift_y = ((HORIZ - py) - HF / 2) / HF

# ---- modelo STL
bpy.ops.wm.stl_import(filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'modelo', 'OctoSmoot.stl'))
raw = bpy.context.selected_objects[0]
bpy.context.view_layer.objects.active = raw
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.separate(type='LOOSE'); bpy.ops.object.mode_set(mode='OBJECT')
parts = [o for o in bpy.data.objects if o.type == 'MESH' and o.data.vertices and o.name.startswith('OctoSmoot')]
def bb(o):
    v = np.array([list(p.co) for p in o.data.vertices]); return v.min(0), v.max(0), len(v)
MAT = {'cuerpo': principled('cuerpo', BODY, 0.42, **{'Specular IOR Level': 0.4}),
       'ojo': principled('ojo', '#101010', 0.25), 'boca': principled('boca', '#CD575B', 0.4), 'anilla': principled('anilla', BODY, 0.42)}
for o in parts:
    lo, hi, n = bb(o); c = (lo + hi) / 2
    kind = 'cuerpo' if n > 5000 else ('anilla' if c[2] > 2.0 else ('ojo' if abs(abs(c[0]) - 0.4) < 0.15 and n < 500 else 'boca'))
    o.data.materials.clear(); o.data.materials.append(MAT[kind]); o.name = 'pulpo_' + kind
    for p_ in o.data.polygons: p_.use_smooth = True
body = [o for o in parts if o.name == 'pulpo_cuerpo'][0]
lo, hi, _ = bb(body); BODY_W = hi[0] - lo[0]
ZMIN = min(bb(o)[0][2] for o in parts); ZMAX = max(bb(o)[1][2] for o in parts)

# tamaño y posición: misma que la caída del anuncio (base en la fila 1720 del vídeo)
px_, pd_ = place(540, 1720)
Wm = px_to_m(360, pd_); K = Wm / BODY_W
H_HALF = (ZMAX - ZMIN) / 2 * K; gz = ground_h(px_, pd_)
pivot = bpy.data.objects.new('pivote', None); scene.collection.objects.link(pivot)
pivot.location = (px_, pd_, gz + H_HALF)
for o in parts:
    o.parent = pivot; o.location = (0, 0, 0)
    o.matrix_parent_inverse = pivot.matrix_world.inverted()
    o.location = (0, 0, 0)
# centrar: el origen del STL está en la base; subimos el modelo para que el pivote quede en el centro vertical
for o in parts:
    o.location = (-(0.0), -(0.0), -( (ZMIN + ZMAX) / 2))
pivot.scale = (K, K, K)

# ---- curvas de movimiento (réplica de las del anuncio en gen_3d.py)
def clamp01(x): return min(1, max(0, x))
def back_out(p, s=2.0): p = p - 1; return p * p * ((s + 1) * p + s) + 1
def elastic_out(p, amp=1.1, per=0.4):
    if p <= 0: return 0
    if p >= 1: return 1
    sft = per / (2 * math.pi) * math.asin(1 / amp); return amp * 2 ** (-10 * p) * math.sin((p - sft) * 2 * math.pi / per) + 1
Z0 = CAM_H + (HORIZ - 820) * pd_ / F_PX            # altura del centro durante el giro (fila 820 del vídeo)
SC = float(arg('--scale', '1.25'))
def state(t):
    py = 780                                                    # cámara de la vista final (playa)
    spin = math.radians(180 + 360 * (1 - (1 - clamp01(t / 2.2)) ** 3))
    sxy, sz, hop = 1.0, 1.0, 0.0
    if 2.35 <= t < 3.1:                                         # salto contento al terminar el giro
        p = (t - 2.35) / 0.75
        hop = 0.28 * math.sin(math.pi * p) * (2 * H_HALF)
        if p < 0.12: sxy, sz = 1 + 0.10 * (p / 0.12), 1 - 0.12 * (p / 0.12)
        elif p > 0.88: q = (p - 0.88) / 0.12; sxy, sz = 1.10 - 0.10 * q, 0.88 + 0.12 * q
    zc = gz + H_HALF * SC * sz + hop
    return py, spin, zc, sxy * SC, sz * SC
def apply(t):
    py, spin, zc, sxy, sz = state(t)
    set_pan(py); pivot.location = (px_, pd_, zc); pivot.rotation_euler = (0, 0, spin); pivot.scale = (K * sxy, K * sxy, K * sz)
    bpy.context.view_layer.update()

FPS = 30
if ONE is not None:
    apply(float(ONE)); scene.render.filepath = os.path.join(OUTD, f'prueba_{ONE}.png'); bpy.ops.render.render(write_still=True)
    print('listo prueba'); sys.exit(0)
T_END = float(arg('--end', '3.1')); n = int(T_END * FPS); I0 = int(arg('--start', '0'))
if '--low' in ARGS:   # tras el aterrizaje: solo la zona de abajo y menos muestras
    scene.render.border_max_y = 0.42; scene.cycles.samples = 32
for i in range(I0, n + 1):
    apply(i / FPS); scene.render.filepath = os.path.join(OUTD, f'f_{i:04d}.png'); bpy.ops.render.render(write_still=True)
json.dump(dict(fps=FPS, frames=n + 1), open(os.path.join(OUTD, 'meta.json'), 'w'))
print('secuencia lista', n + 1)
