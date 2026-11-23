#!/usr/bin/env python3
"""Fases del nacimiento de Octo en 3D (Blender 5.1.2, bpy): 9 bolas sueltas, cuerpo fundido, +ojos, +boca, +anilla y 4 combinaciones de color.
Salida: PNG transparentes con la misma cámara (ortográfica, algo desde arriba). Uso: python proceso.py <salida> [--preview] [--only nombre,nombre]"""
import bpy, math, os, sys
import numpy as np
from mathutils import Vector
OUT = sys.argv[1]; PREV = '--preview' in sys.argv
ONLY = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
STL = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'OctoSmoot.stl')
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 24 if PREV else 40; sc.cycles.use_denoising = True
sc.render.resolution_x = 540 if PREV else 1080; sc.render.resolution_y = 960 if PREV else 1920; sc.render.resolution_percentage = 100
sc.view_settings.view_transform = 'Standard'; sc.render.film_transparent = True
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
def hexrgb(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return (*[x / 12.92 if x <= 0.04045 else ((x + .055) / 1.055) ** 2.4 for x in c], 1.0)
def mat(name, color, rough=0.42):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = hexrgb(color); b.inputs['Roughness'].default_value = rough
    if 'Specular IOR Level' in b.inputs: b.inputs['Specular IOR Level'].default_value = 0.4
    return m
# mundo y luz
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (1, 1, 1, 1); bg.inputs['Strength'].default_value = 0.6
sun_d = bpy.data.lights.new('s', 'SUN'); sun_d.energy = 3.0; sun_d.angle = math.radians(18); sun = bpy.data.objects.new('s', sun_d); sc.collection.objects.link(sun)
sun.rotation_euler = Vector((0.45, 0.55, -0.6)).normalized().to_track_quat('-Z', 'Y').to_euler()
# cámara ortográfica algo desde arriba
cd = bpy.data.cameras.new('c'); cd.type = 'ORTHO'; cd.ortho_scale = 6.34; cam = bpy.data.objects.new('c', cd); sc.collection.objects.link(cam); sc.camera = cam
TGT = Vector((0, 0, 0.92)); el = math.radians(9); dist = 12
cam.location = TGT + Vector((0, -dist * math.cos(el), dist * math.sin(el)))
cam.rotation_euler = ((TGT - cam.location).to_track_quat('-Z', 'Y')).to_euler()
# STL
bpy.ops.wm.stl_import(filepath=STL); raw = bpy.context.selected_objects[0]; bpy.context.view_layer.objects.active = raw
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.separate(type='LOOSE'); bpy.ops.object.mode_set(mode='OBJECT')
P = {'cuerpo': [], 'ojo': [], 'boca': [], 'anilla': []}
for o in [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith('OctoSmoot')]:
    v = np.array([list(p.co) for p in o.data.vertices]); c = (v.min(0) + v.max(0)) / 2; n = len(v)
    k = 'cuerpo' if n > 5000 else ('anilla' if c[2] > 2.0 else ('ojo' if abs(abs(c[0]) - 0.4) < 0.15 and n < 500 else 'boca'))
    P[k].append(o); o.rotation_euler = (0, 0, math.pi); o.hide_render = True
    for p in o.data.polygons: p.use_smooth = True
# bolas sueltas (metaballs aproximadas): cabeza + 8 brazos
BALLS = [('cabeza', (0, 0, 1.30), 1.00)]
for k in range(8):
    a = math.radians(22.5 + 45 * k); BALLS.append((f'brazo{k}', (0.84 * math.cos(a), 0.84 * math.sin(a), 0.34), 0.42))
SPH = {}
for nme, loc, r in BALLS:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=64, ring_count=32); s = bpy.context.object; s.name = nme; s.hide_render = True
    for p in s.data.polygons: p.use_smooth = True
    SPH[nme] = s
CLAY = mat('clay', '#E4E0F0', 0.6); DARK = mat('dark', '#2A2830', 0.3)
def setmat(objs, m):
    for o in objs: o.data.materials.clear(); o.data.materials.append(m)
def hide_all():
    for l in P.values():
        for o in l: o.hide_render = True
    for s in SPH.values(): s.hide_render = True
def show(*keys):
    for k in keys:
        for o in P[k]: o.hide_render = False
def shot(name):
    if ONLY and name not in ONLY: return
    sc.render.use_border = True; sc.render.use_crop_to_border = False
    sc.render.border_min_x, sc.render.border_max_x, sc.render.border_min_y, sc.render.border_max_y = 0.04, 0.96, 0.22, 0.80
    sc.render.filepath = os.path.join(OUT, name + '.png'); bpy.ops.render.render(write_still=True); print('listo', name)
# 1) bolas sueltas
for nme in SPH:
    hide_all(); SPH[nme].hide_render = False; setmat([SPH[nme]], CLAY); shot('bola_' + nme)
# 2) cuerpo fundido y detalles acumulados (arcilla)
for k in ('cuerpo', 'ojo', 'boca', 'anilla'): setmat(P[k], CLAY)
setmat(P['ojo'], DARK)
hide_all(); show('cuerpo'); shot('cuerpo')
hide_all(); show('cuerpo', 'ojo'); shot('ojos')
hide_all(); show('cuerpo', 'ojo', 'boca'); shot('boca')
hide_all(); show('cuerpo', 'ojo', 'boca', 'anilla'); shot('anilla')
# 3) colores
COL = {'violeta': ('#7051C4', '#CD575B'), 'rosa': ('#F28FA8', '#C84A6C'), 'violeta_rosa': ('#7051C4', '#F08FA6')}
for nme, (cb, cm) in COL.items():
    setmat(P['cuerpo'], mat('b_' + nme, cb)); setmat(P['anilla'], mat('a_' + nme, cb)); setmat(P['boca'], mat('m_' + nme, cm, 0.4)); setmat(P['ojo'], mat('o_' + nme, '#101010', 0.25))
    hide_all(); show('cuerpo', 'ojo', 'boca', 'anilla'); shot('col_' + nme)
