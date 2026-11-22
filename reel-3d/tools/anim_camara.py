#!/usr/bin/env python3
"""Anuncio OctoMood con cámara en movimiento (Blender 5.1.2, bpy):
 A (0-1,9 s)  cámara fija a la altura del pulpo, algo cerca: giro rápido→lento. Fondo + pulpo con alfa por separado.
 B (1,9-4,0 s) la cámara baja con el pulpo, él aterriza (aplasta y rebota) y la cámara se abre hacia atrás y arriba; aparecen las siluetas.
Uso: python anim_camara.py <salida> [--preview] [--mode bgA|A|B|all] [--frame T] [--body #7051C4]
Salida: bgA.png, A_%04d.png (alfa), B_%04d.png (escena completa), meta.json"""
import sys, os, math, json
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'escena_playa.py')).read()
ARGS = sys.argv[:]
OUTD = ARGS[1]; PREV = '--preview' in ARGS
def arg(n, d=None): return ARGS[ARGS.index(n) + 1] if n in ARGS else d
BODY = arg('--body', '#7051C4'); RESUME = '--resume' in ARGS; MODE = arg('--mode', 'all'); ONE = arg('--frame')
sys.argv = ['x', '/tmp/claude-0/escena_tmp', '--only', 'none'] + (['--preview'] if PREV else [])
exec(compile(SRC, 'escena_playa', 'exec'))
import numpy as np
os.makedirs(OUTD, exist_ok=True)
sun_d.angle = math.radians(22)

# ---------------------------------------------------------------- cámara de vídeo 1080x1920
HF = 1920; RES2 = 0.5 if PREV else 1.0
scene.render.resolution_x = int(1080 * RES2); scene.render.resolution_y = int(HF * RES2); scene.render.resolution_percentage = 100
cam_d.sensor_height = 36.0 * HF / 2700.0
scene.cycles.samples = 12 if PREV else 14
scene.render.use_persistent_data = True      # reutiliza la escena entre fotogramas (mucho más rápido)
scene.cycles.use_adaptive_sampling = True
HR0, HR1 = 930.0, 920.0                 # fila del horizonte al empezar / al final
CAM_Y0 = 2.4                            # al empezar la cámara está más cerca del pulpo (m)
def set_cam(y, z, hr):
    cam.location = (0.0, y, z); cam_d.shift_y = (hr - HF / 2) / HF

# ---------------------------------------------------------------- pulpo (STL de Avril)
bpy.ops.wm.stl_import(filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'modelo', 'OctoSmoot.stl'))
raw = [o for o in bpy.context.selected_objects][0]; bpy.context.view_layer.objects.active = raw
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.separate(type='LOOSE'); bpy.ops.object.mode_set(mode='OBJECT')
parts = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith('OctoSmoot') and o.data.vertices and not o.hide_render]
MAT = {'cuerpo': principled('cuerpo', BODY, 0.42, **{'Specular IOR Level': 0.4}), 'ojo': principled('ojo', '#101010', 0.25),
       'boca': principled('boca', '#CD575B', 0.4), 'anilla': principled('anilla', BODY, 0.42)}
for o in parts:
    v = np.array([list(p_.co) for p_ in o.data.vertices]); c = (v.min(0) + v.max(0)) / 2; n_ = len(v)
    kind = 'cuerpo' if n_ > 5000 else ('anilla' if c[2] > 2.0 else ('ojo' if abs(abs(c[0]) - 0.4) < 0.15 and n_ < 500 else 'boca'))
    o.data.materials.clear(); o.data.materials.append(MAT[kind]); o.name = 'pulpo_' + kind
    for p_ in o.data.polygons: p_.use_smooth = True
    o.hide_viewport = False; o.hide_render = False
ZMIN, ZMAX, BODY_W = -0.084, 2.6, 2.64
px_, pd_ = place(540, 1720)
Wm = px_to_m(360, pd_); K = Wm / BODY_W; H_HALF = (ZMAX - ZMIN) / 2 * K; gz = ground_h(px_, pd_)
pivot = bpy.data.objects.new('pivote', None); scene.collection.objects.link(pivot)
for o in parts:
    o.parent = pivot; o.location = (0, 0, -((ZMIN + ZMAX) / 2))
def clamp01(x): return min(1, max(0, x))
def back_out(p, s=2.0): p = p - 1; return p * p * ((s + 1) * p + s) + 1
def elastic_out(p, amp=1.1, per=0.4):
    if p <= 0: return 0
    if p >= 1: return 1
    sft = per / (2 * math.pi) * math.asin(1 / amp); return amp * 2 ** (-10 * p) * math.sin((p - sft) * 2 * math.pi / per) + 1
def inout(p): p = clamp01(p); return 2 * p * p if p < .5 else 1 - (-2 * p + 2) ** 2 / 2
ZL = gz + H_HALF                         # altura del centro del pulpo posado
Z0 = 3.4                                 # altura del giro (la cámara está a esta altura)

# siluetas: aparición con rebote (escala desde la base)
POP = {'s1': 2.95, 's2': 3.10, 's4': 3.25, 's5': 3.40, 's3': 3.60}
TOY = {}
for k in POP:
    root, prts, _ = objs[k]; base = Vector((root.location.x, root.location.y, root.location.z)); K0 = root.scale.x
    q = [o for o in prts if o.name.endswith('_q')][0]; TOY[k] = (root, q, base, K0, Vector(q.location), q.scale.copy(), [o for o in prts])

def pose(t):
    """Estado en el instante t (s): pulpo + cámara + siluetas."""
    pop = 0.5 + 0.5 * back_out(clamp01(t / 0.4)) if t < 0.4 else 1.0
    spin = math.radians(180 + 720 * (1 - (1 - clamp01((t - 0.1) / 1.8)) ** 3))
    zc = Z0 + (ZL - Z0) * clamp01((t - 1.9) / 0.65) ** 2                 # caída (misma curva que antes)
    sxy = sz = 1.0
    if t >= 2.55:
        a = clamp01((t - 2.55) / 0.09); b = elastic_out(clamp01((t - 2.64) / 0.35)); sq = (1.12, 0.82)
        if t < 2.64: sxy, sz = 1 + (sq[0] - 1) * (1 - (1 - a) ** 2), 1 + (sq[1] - 1) * (1 - (1 - a) ** 2)
        else: sxy, sz = sq[0] + (1 - sq[0]) * b, sq[1] + (1 - sq[1]) * b
        zc = gz + H_HALF * sz
    cam_z = zc if t < 2.55 else ZL                                         # la cámara baja con el pulpo y se queda a su altura
    e = inout((t - 2.75) / 1.15)                                           # apertura: atrás y arriba
    cam_y = CAM_Y0 * (1 - e); cam_z = cam_z + (CAM_H - cam_z) * e; hr = HR0 + (HR1 - HR0) * e
    return dict(pop=pop, spin=spin, zc=zc, sxy=sxy, sz=sz, cam=(cam_y, cam_z, hr))
def apply(t, show_toys=True, show_octo=True):
    st = pose(t); set_cam(*st['cam'])
    pivot.location = (px_, pd_, st['zc']); pivot.rotation_euler = (0, 0, st['spin'])
    pivot.scale = (K * st['sxy'] * st['pop'], K * st['sxy'] * st['pop'], K * st['sz'] * st['pop'])
    for o in parts: o.hide_render = not show_octo
    for k, (root, q, base, K0, qloc, qscale, prts) in TOY.items():
        f = 0.0 if t < POP[k] else 0.3 + 0.7 * back_out(clamp01((t - POP[k]) / 0.32))
        vis_ = show_toys and t >= POP[k]
        for o in prts: o.hide_render = not vis_
        root.scale = (K0 * f, K0 * f, K0 * f); q.scale = qscale * f; q.location = base + (qloc - base) * f
    bpy.context.view_layer.update()

def render(path, transparent):
    scene.render.film_transparent = transparent; scene.render.image_settings.color_mode = 'RGBA' if transparent else 'RGB'
    scene.render.filepath = path; bpy.ops.render.render(write_still=True)

def scene_mode(kind):
    """kind: 'bg' = solo fondo; 'octo' = pulpo con sombra, transparente; 'full' = todo."""
    full = kind in ('bg', 'full')
    sand.is_shadow_catcher = (kind == 'octo')
    for ob in (sea, foam, sol): ob.hide_render = (kind == 'octo')
    for o in bpy.data.objects:
        if o.name.startswith('Sphere') or o.name.startswith('estrella'): o.hide_render = (kind == 'octo')
    proxy.hide_render = True

if ONE is not None:
    scene_mode('full'); apply(float(ONE), True, True); render(os.path.join(OUTD, f'prueba_{ONE}.png'), False); print('listo prueba'); sys.exit(0)

FPS = 30; N_A = int(1.9 * FPS); N_B0, N_B1 = N_A, int(4.0 * FPS)
if MODE in ('bgA', 'all') and not (RESUME and os.path.exists(os.path.join(OUTD, 'bgA.png'))):
    scene_mode('bg'); apply(0.5, False, False); render(os.path.join(OUTD, 'bgA.png'), False); print('bgA listo')
if MODE in ('A', 'all'):
    scene_mode('octo')
    scene.render.use_border = True; scene.render.use_crop_to_border = False       # solo la zona donde está el pulpo (ahorra tiempo)
    scene.render.border_min_x, scene.render.border_max_x, scene.render.border_min_y, scene.render.border_max_y = 0.08, 0.95, 0.0, 0.72
    for i in range(0, N_A):
        if os.path.exists(os.path.join(OUTD, f'A_{i:04d}.png')) and i < N_A - 1 and os.path.getsize(os.path.join(OUTD, f'A_{i:04d}.png')) > 1000 and RESUME: continue
        apply(i / FPS, False, True); render(os.path.join(OUTD, f'A_{i:04d}.png'), True)
    print('A listo')
if MODE in ('B', 'all'):
    scene.render.use_border = False
    scene_mode('full')
    for i in range(N_B0, N_B1 + 1):
        if os.path.exists(os.path.join(OUTD, f'B_{i:04d}.png')) and RESUME: continue
        apply(i / FPS, True, True); render(os.path.join(OUTD, f'B_{i:04d}.png'), False)
    print('B listo')
json.dump(dict(fps=FPS, nA=N_A, b0=N_B0, b1=N_B1), open(os.path.join(OUTD, 'meta.json'), 'w'))
