#!/usr/bin/env python3
"""Playa 3D para el anuncio OctoMood (Blender 5.x, módulo bpy).
Uso:  python escena_playa.py <carpeta de salida> [--preview] [--only bg|capas]
Genera: fondo.png (1080x2700, cielo+mar+arena con relieve) y capas PNG transparentes (siluetas 3D con su sombra
y la sombra del pulpo morado) + capas.json con la posición de cada capa."""
import bpy, bmesh, math, json, sys, os
import numpy as np
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
PREVIEW = '--preview' in sys.argv
ONLY = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else 'all'
W, H = 1080, 2700
RES = 0.4 if PREVIEW else 1.0
SAMPLES = 20 if PREVIEW else 72
F_PX = 35.0 / 36.0 * H            # focal en píxeles (lente 35 mm, sensor vertical 36 mm)
CAM_H = 1.5                        # altura de la cámara (m)
HORIZ = 1700                       # fila del horizonte en el fondo alto
PAN = 780                          # el vídeo baja 780 px: fila_fondo = fila_vídeo + PAN
FONT = '/tmp/claude-0/BagelFatOne.ttf'
SAND, SEA, YEL, DBLUE, BLACK, CORAL = '#FEF3C9', '#8DD0F7', '#FFD84D', '#1F5F93', '#141414', '#CD575B'

def hexrgb(h, a=1.0):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    lin = [x / 12.92 if x <= 0.04045 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return (*lin, a)

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
reset()
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = SAMPLES
scene.cycles.use_denoising = True
try: scene.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
scene.cycles.max_bounces = 6
scene.render.resolution_x = int(W * RES); scene.render.resolution_y = int(H * RES); scene.render.resolution_percentage = 100
scene.view_settings.view_transform = 'Standard'; scene.view_settings.look = 'None'
scene.render.image_settings.file_format = 'PNG'; scene.render.image_settings.color_depth = '8'

# ---------------------------------------------------------------- utilidades de proyección
def place(x_px, base_final_y):
    """Punto del suelo (X, Y en m) que se ve en la columna x_px y la fila base_final_y del vídeo."""
    row = base_final_y + PAN
    d = CAM_H * F_PX / (row - HORIZ)
    return (x_px - W / 2) * d / F_PX, d

def px_to_m(px, d): return px * d / F_PX

# ---------------------------------------------------------------- cámara
cam_d = bpy.data.cameras.new('cam'); cam_d.lens = 35; cam_d.sensor_fit = 'VERTICAL'; cam_d.sensor_height = 36
cam_d.clip_end = 2000
cam = bpy.data.objects.new('cam', cam_d); scene.collection.objects.link(cam); scene.camera = cam
cam.location = (0, 0, CAM_H); cam.rotation_euler = (math.radians(90), 0, 0)
cam_d.shift_y = (H / 2 - HORIZ) / H * -1.0 * -1.0    # se afina abajo con una prueba del horizonte
def horizon_row():
    p = world_to_camera_view(scene, cam, Vector((0, 5000, 0)))
    return (1 - p.y) * H
cam_d.shift_y = 0.0
r0 = horizon_row()
cam_d.shift_y = (HORIZ - r0) / H          # positivo: el horizonte baja
print('horizonte en fila', round(horizon_row()), '(objetivo', HORIZ, ')')

# ---------------------------------------------------------------- mundo (cielo degradado) y sol
world = bpy.data.worlds.new('w'); scene.world = world; world.use_nodes = True
nt = world.node_tree; nt.nodes.clear()
bg = nt.nodes.new('ShaderNodeBackground'); out = nt.nodes.new('ShaderNodeOutputWorld')
tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); ramp = nt.nodes.new('ShaderNodeValToRGB')
nt.links.new(tc.outputs['Generated'], sep.inputs[0]); nt.links.new(sep.outputs['Z'], ramp.inputs['Fac'])
ramp.color_ramp.elements[0].position = 0.5; ramp.color_ramp.elements[0].color = hexrgb('#C4E9FC')
e = ramp.color_ramp.elements.new(0.62); e.color = hexrgb('#B6E4FD')
ramp.color_ramp.elements[-1].position = 0.8; ramp.color_ramp.elements[-1].color = hexrgb('#9ED6F9')
nt.links.new(ramp.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = 1.0
bg2 = nt.nodes.new('ShaderNodeBackground'); bg2.inputs['Color'].default_value = (1, 1, 1, 1); bg2.inputs['Strength'].default_value = 0.5
lp = nt.nodes.new('ShaderNodeLightPath'); mxr = nt.nodes.new('ShaderNodeMath'); mxr.operation = 'MAXIMUM'
nt.links.new(lp.outputs['Is Camera Ray'], mxr.inputs[0]); nt.links.new(lp.outputs['Is Glossy Ray'], mxr.inputs[1])
mxs = nt.nodes.new('ShaderNodeMixShader'); nt.links.new(mxr.outputs[0], mxs.inputs['Fac'])
nt.links.new(bg2.outputs[0], mxs.inputs[1]); nt.links.new(bg.outputs[0], mxs.inputs[2])
nt.links.new(mxs.outputs[0], out.inputs[0])

sun_d = bpy.data.lights.new('sol', 'SUN'); sun_d.energy = 3.3; sun_d.angle = math.radians(9); sun_d.color = (1.0, 0.95, 0.84)
sun = bpy.data.objects.new('sol', sun_d); scene.collection.objects.link(sun)
sun.rotation_euler = Vector((0.5, 0.6, -0.5)).normalized().to_track_quat('-Z', 'Y').to_euler()

# ---------------------------------------------------------------- materiales
def principled(name, color, rough=0.5, **kw):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = hexrgb(color); b.inputs['Roughness'].default_value = rough
    for k, v in kw.items():
        if k in b.inputs: b.inputs[k].default_value = v
    return m

def toy(name, color):
    return principled(name, color, 0.28, **{'Coat Weight': 0.5, 'Coat Roughness': 0.15, 'Subsurface Weight': 0.08})

def sand_material():
    m = bpy.data.materials.new('arena'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc = nt.nodes.new('ShaderNodeTexCoord'); n1 = nt.nodes.new('ShaderNodeTexNoise'); n2 = nt.nodes.new('ShaderNodeTexNoise'); n3 = nt.nodes.new('ShaderNodeTexNoise')
    n1.inputs['Scale'].default_value = 0.9; n1.inputs['Detail'].default_value = 3
    n2.inputs['Scale'].default_value = 260; n2.inputs['Detail'].default_value = 5      # grano
    n3.inputs['Scale'].default_value = 24; n3.inputs['Detail'].default_value = 3       # granulado medio
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = hexrgb('#FFF0BF'); cr.color_ramp.elements[1].color = hexrgb('#FFF9DC')
    for nn in (n1, n2, n3): nt.links.new(tc.outputs['Object'], nn.inputs['Vector'])
    nt.links.new(n1.outputs['Fac'], cr.inputs['Fac'])
    ao = nt.nodes.new('ShaderNodeAmbientOcclusion'); ao.inputs['Distance'].default_value = 0.35
    mao = nt.nodes.new('ShaderNodeMix'); mao.data_type = 'RGBA'
    nt.links.new(ao.outputs['AO'], mao.inputs['Factor']); mao.inputs[6].default_value = hexrgb('#E9D29A'); nt.links.new(cr.outputs['Color'], mao.inputs[7])
    geo = nt.nodes.new('ShaderNodeNewGeometry'); sp = nt.nodes.new('ShaderNodeSeparateXYZ'); wet = nt.nodes.new('ShaderNodeMapRange')
    nt.links.new(geo.outputs['Position'], sp.inputs[0]); nt.links.new(sp.outputs['Y'], wet.inputs['Value'])
    wet.inputs['From Min'].default_value = 17.6; wet.inputs['From Max'].default_value = 19.6; wet.inputs['To Min'].default_value = 0; wet.inputs['To Max'].default_value = 1
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    nt.links.new(wet.outputs['Result'], mix.inputs['Factor']); nt.links.new(mao.outputs[2], mix.inputs[6]); mix.inputs[7].default_value = hexrgb('#EAD293')
    gsum = nt.nodes.new('ShaderNodeMath'); gsum.operation = 'ADD'
    g2 = nt.nodes.new('ShaderNodeMath'); g2.operation = 'MULTIPLY'; g2.inputs[1].default_value = 0.6
    nt.links.new(n3.outputs['Fac'], g2.inputs[0]); nt.links.new(n2.outputs['Fac'], gsum.inputs[0]); nt.links.new(g2.outputs[0], gsum.inputs[1])
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.35; bump.inputs['Distance'].default_value = 0.012
    nt.links.new(gsum.outputs[0], bump.inputs['Height'])
    nt.links.new(mix.outputs[2], b.inputs['Base Color']); nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    b.inputs['Roughness'].default_value = 0.9
    nt.links.new(b.outputs[0], o.inputs[0])
    return m

def sea_material():
    m = bpy.data.materials.new('mar'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value = hexrgb('#3FA8EE'); b.inputs['Roughness'].default_value = 0.22
    tc = nt.nodes.new('ShaderNodeTexCoord'); n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 2.5; n.inputs['Detail'].default_value = 5
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1, 0.15, 1)    # olas alargadas
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.35
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], n.inputs['Vector'])
    nt.links.new(n.outputs['Fac'], bump.inputs['Height']); nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    nt.links.new(b.outputs[0], o.inputs[0])
    return m

def foam_material():
    m = bpy.data.materials.new('espuma'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value = hexrgb('#FFFFFF'); b.inputs['Roughness'].default_value = 0.6
    b.inputs['Emission Color'].default_value = hexrgb('#FFFFFF'); b.inputs['Emission Strength'].default_value = 0.35
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
    tc = nt.nodes.new('ShaderNodeTexCoord'); n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 9; n.inputs['Detail'].default_value = 8
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (0.6, 4.0, 1)
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.45; cr.color_ramp.elements[1].position = 0.62
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], n.inputs['Vector'])
    nt.links.new(n.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], mx.inputs['Fac'])
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(b.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], o.inputs[0])
    return m

# ---------------------------------------------------------------- arena: relieve irregular y suave (dunas redondeadas, hondonadas, grano fino)
def _perlin_setup(seed):
    rng = np.random.default_rng(seed); perm = rng.permutation(256); perm = np.concatenate([perm, perm])
    ang = rng.uniform(0, 2 * np.pi, 256); return perm, np.cos(ang), np.sin(ang)
_P = {}
def perlin(x, y, seed):
    if seed not in _P: _P[seed] = _perlin_setup(seed)
    perm, gx, gy = _P[seed]
    xi = np.floor(x).astype(int); yi = np.floor(y).astype(int); xf = x - xi; yf = y - yi
    def g(ix, iy, dx, dy):
        h = perm[(perm[ix & 255] + iy) & 255]; return gx[h] * dx + gy[h] * dy
    u = xf * xf * xf * (xf * (xf * 6 - 15) + 10); v = yf * yf * yf * (yf * (yf * 6 - 15) + 10)
    n00 = g(xi, yi, xf, yf); n10 = g(xi + 1, yi, xf - 1, yf); n01 = g(xi, yi + 1, xf, yf - 1); n11 = g(xi + 1, yi + 1, xf - 1, yf - 1)
    return (n00 * (1 - u) + n10 * u) * (1 - v) + (n01 * (1 - u) + n11 * u) * v

def relief(X, Y):
    """Altura natural de la arena (m): dunas grandes, lomas medias deformadas por el viento y hondonadas suaves."""
    X = np.asarray(X, float); Y = np.asarray(Y, float)
    wx = perlin(X / 5.0, Y / 5.0, 21) * 1.6; wy = perlin(X / 5.0 + 9.3, Y / 5.0 + 4.1, 22) * 1.6        # deformación del dominio
    big = perlin((X + wx) / 4.2, (Y + wy) / 3.4, 1) * 0.30                                              # dunas grandes
    mid = perlin((X + wy * .5) / 1.25, (Y + wx * .5) / 0.95, 2) * 0.085                                  # lomas medias
    mid2 = np.tanh(perlin(X / 0.55 + wx, Y / 0.42 + wy, 3) * 1.6) * 0.022                               # pliegues redondeados
    fine = perlin(X / 0.16, Y / 0.16, 4) * 0.004                                                         # ondulación del grano
    return big + mid + mid2 + fine

FLATS = []       # (x, y, radio): se aplana suavemente la arena bajo cada juguete
def height(X, Y):
    h = relief(X, Y); X = np.asarray(X, float); Y = np.asarray(Y, float)
    for fx, fy, fr in FLATS:
        hc = float(relief(np.array(fx), np.array(fy)))
        m = np.exp(-((X - fx) ** 2 + (Y - fy) ** 2) / (2 * (fr * 0.6) ** 2))
        h = h * (1 - m) + hc * m
    fade = 1 - np.clip((Y - 12.0) / 6.5, 0, 1)                      # el relieve se aplana hacia la orilla
    h = h * fade
    base = np.where(Y < 18.0, 0.0, np.where(Y < 19.7, -0.04 * (Y - 18.0) / 1.7, -0.04 - 0.30 * (Y - 19.7)))
    return h + base

def build_sand():
    nx, ny = 421, 640
    xs = np.linspace(-10, 10, nx); t = np.linspace(0, 1, ny); ys = 0.3 + 21.7 * t ** 1.7        # más densa cerca de la cámara
    X, Y = np.meshgrid(xs, ys); Z = height(X, Y)
    verts = np.stack([X, Y, Z], -1).reshape(-1, 3).tolist()
    idx = np.arange(nx * ny).reshape(ny, nx)
    faces = np.stack([idx[:-1, :-1], idx[:-1, 1:], idx[1:, 1:], idx[1:, :-1]], -1).reshape(-1, 4).tolist()
    me = bpy.data.meshes.new('arena'); me.from_pydata(verts, [], faces); me.update()
    ob = bpy.data.objects.new('arena', me); scene.collection.objects.link(ob)
    for p in me.polygons: p.use_smooth = True
    ob.data.materials.append(sand_material())
    return ob, (lambda x, y: float(height(np.array(x), np.array(y))))

# posiciones de los juguetes (antes de construir la arena, para aplanar bajo ellos)
_SIL_POS = {'s1': (135, 1760, 170), 's2': (270, 1640, 150), 's4': (810, 1640, 150), 's5': (945, 1760, 170), 's3': (540, 1545, 160)}
for _k, (_x, _y, _w) in _SIL_POS.items():
    _X, _D = place(_x, _y); FLATS.append((_X, _D, px_to_m(_w, _D) * 0.9))
_X, _D = place(540, 1900); FLATS.append((_X, _D, px_to_m(360, _D) * 0.8))
sand, ground_h = build_sand()

# mar y espuma
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 260, -0.04)); sea = bpy.context.object; sea.name = 'mar'; sea.scale = (900, 480, 1)
sea.data.materials.append(sea_material())
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 19.62, -0.035)); foam = bpy.context.object; foam.name = 'espuma'; foam.scale = (60, 0.45, 1)
foam.data.materials.append(foam_material())

# ---------------------------------------------------------------- sol y nubes en 3D
def sky_dir(px, row, dist):
    x = (px - W / 2) / F_PX; z = (HORIZ - row) / F_PX
    v = Vector((x, 1.0, z)).normalized(); return v * dist
sun_pos = sky_dir(895, 255, 220)
bpy.ops.mesh.primitive_circle_add(radius=0.0876 * 220 / 2, location=sun_pos, vertices=96, fill_type='NGON', rotation=(math.radians(90), 0, 0)); sol = bpy.context.object; sol.name = 'disco_sol'
sm = bpy.data.materials.new('sol'); sm.use_nodes = True; b = sm.node_tree.nodes['Principled BSDF']
b.inputs['Base Color'].default_value = hexrgb('#FFE98A'); b.inputs['Emission Color'].default_value = hexrgb('#FFE98A'); b.inputs['Emission Strength'].default_value = 1.2
sol.data.materials.append(sm); sol.visible_shadow = False

cloud_mat = principled('nube', '#FFFFFF', 1.0, **{'Emission Color': hexrgb('#FFFFFF'), 'Emission Strength': 0.25})
def cloud(px, row, wpx, dist=110):
    c = sky_dir(px, row, dist); w = wpx * dist / F_PX
    for dx, r, dz in ((-.36, .12, 0), (-.17, .19, .05), (.02, .25, .07), (.22, .19, .04), (.38, .12, 0)):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r * w, location=(c.x + dx * w, c.y + (dx * 0.2) * w, c.z + dz * w), segments=40, ring_count=20)
        s = bpy.context.object; s.scale.z = 0.72; s.data.materials.append(cloud_mat)
        for p in s.data.polygons: p.use_smooth = True
cloud(190, 560, 330); cloud(790, 820, 400); cloud(330, 1260, 280); cloud(930, 1380, 240)

# ---------------------------------------------------------------- pequeños detalles en la arena (estrellas de mar y conchas)
def starfish(px, row, w_m, color=CORAL):
    x, d = place(px, row)
    me = bpy.data.meshes.new('estrella'); bm = bmesh.new()
    pts = []
    for k in range(10):
        r = 1.0 if k % 2 == 0 else 0.46; a = math.radians(90 + k * 36); pts.append((math.cos(a) * r, math.sin(a) * r))
    vs = [bm.verts.new((px_, py_, 0)) for px_, py_ in pts]
    bm.faces.new(vs); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new('estrella', me); scene.collection.objects.link(ob)
    mod = ob.modifiers.new('s', 'SOLIDIFY'); mod.thickness = 0.35; mod.offset = 0
    bev = ob.modifiers.new('b', 'BEVEL'); bev.width = 0.08; bev.segments = 3
    sub = ob.modifiers.new('ss', 'SUBSURF'); sub.levels = 2
    ob.scale = (w_m / 2, w_m / 2, w_m / 2); ob.location = (x, d, ground_h(x, d) + 0.03); ob.rotation_euler = (0, math.radians(-8), math.radians(25))
    ob.data.materials.append(toy('estrella', color))
    for p in me.polygons: p.use_smooth = True
starfish(70, 1460, 0.26); starfish(1015, 1300, 0.2, '#FFD84D')
for o in bpy.data.objects:
    if o.name.startswith('estrella'):
        q = world_to_camera_view(scene, cam, o.location); print('estrella', o.name, tuple(round(v, 2) for v in o.location), 'px', round(q.x * W), round((1 - q.y) * H) - PAN)

# ---------------------------------------------------------------- siluetas 3D (misma forma que el envoltorio)
SVG = [(262, 195, 180), (115, 328, 58), (410, 328, 58), (196, 358, 66), (330, 358, 66)]   # cx, cy, r en el dibujo
def silueta(name, x_px, base_final_y, w_px, color, qcolor):
    x, d = place(x_px, base_final_y); Wm = px_to_m(w_px, d); s = Wm / 411.0
    root = bpy.data.objects.new(name, None); scene.collection.objects.link(root); root.location = (x, d, ground_h(x, d))
    mat = toy(name + '_m', color); parts = []
    for cx, cy, r in SVG:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r * s, location=(x + (cx - 262.5) * s, d, root.location.z + (424 - cy) * s), segments=48, ring_count=24)
        o = bpy.context.object; o.data.materials.append(mat); o.parent = root; o.matrix_parent_inverse = root.matrix_world.inverted()
        for p in o.data.polygons: p.use_smooth = True
        parts.append(o)
    # signo de interrogación en relieve sobre la cabeza
    cu = bpy.data.curves.new(name + '_q', 'FONT'); cu.body = '?'; cu.size = 0.41 * Wm; cu.extrude = 0.035 * Wm; cu.bevel_depth = 0.006 * Wm
    cu.align_x = 'CENTER'; cu.align_y = 'CENTER'
    try: cu.font = bpy.data.fonts.load(FONT)
    except Exception as ex: print('fuente:', ex)
    q = bpy.data.objects.new(name + '_q', cu); scene.collection.objects.link(q)
    q.rotation_euler = (math.radians(90), 0, 0); q.location = (x, d - 180 * s * 0.965, root.location.z + (424 - 212) * s)
    q.parent = root; q.matrix_parent_inverse = root.matrix_world.inverted(); q.data.materials.append(toy(name + '_qm', qcolor)); parts.append(q)
    return root, parts, Wm

SIL = {
    's1': (135, 1760, 170, YEL, DBLUE), 's2': (270, 1640, 150, YEL, DBLUE),
    's4': (810, 1640, 150, YEL, DBLUE), 's5': (945, 1760, 170, YEL, DBLUE),
    's3': (540, 1545, 160, BLACK, YEL),
}
objs = {k: silueta(k, *v) for k, v in SIL.items()}
# proxy invisible para la sombra del pulpo morado (su imagen 2D la pone el montaje)
px_, pd_ = place(540, 1900)
Wp = px_to_m(360, pd_)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(px_, pd_, ground_h(px_, pd_) + 0.46 * Wp), segments=48, ring_count=24)
proxy = bpy.context.object; proxy.name = 'sombra_morado'; proxy.scale = (0.5 * Wp, 0.42 * Wp, 0.5 * Wp)

def vis(show_names, catcher):
    for k, (root, parts, _) in objs.items():
        for o in parts: o.hide_render = (k not in show_names); o.visible_camera = True
    proxy.hide_render = ('morado' not in show_names)
    proxy.visible_camera = False
    sand.is_shadow_catcher = catcher
    for ob in (sea, foam, sol): ob.hide_render = catcher
    for o in bpy.data.objects:
        if o.name.startswith('Sphere') and o.name not in [p.name for _, ps, _ in objs.values() for p in ps]: o.hide_render = catcher
        if o.name.startswith('estrella'): o.hide_render = catcher

def render_to(path, border=None, transparent=False):
    scene.render.film_transparent = transparent
    scene.render.use_border = border is not None
    if border:
        scene.render.border_min_x, scene.render.border_min_y, scene.render.border_max_x, scene.render.border_max_y = border
        scene.render.use_crop_to_border = True
    scene.render.image_settings.color_mode = 'RGBA' if transparent else 'RGB'
    scene.render.filepath = path; bpy.ops.render.render(write_still=True)

if ONLY in ('all', 'bg'):
    vis([], False)
    for _, ps, _ in objs.values():
        for o in ps: o.hide_render = True
    proxy.hide_render = True
    sand.is_shadow_catcher = False
    render_to(os.path.join(OUT, 'fondo.png'))

if ONLY in ('all', 'capas'):
    meta = {}
    capas = [(k, [k]) for k in objs] + [('morado', ['morado'])]
    for k, show in capas:
        vis(show, True)
        pts = []
        if k == 'morado':
            Wm = Wp; cx, cy = px_, pd_
            for dx in (-0.8, 1.9):
                for dy in (-0.5, 1.4):
                    for dz in (0, 0.5):
                        pts.append(Vector((cx + dx * Wm, cy + dy * Wm, ground_h(cx, cy) + dz * Wm)))
        else:
            root, parts, Wm = objs[k]; cx, cy = root.location.x, root.location.y
            for dx in (-0.7, 1.9):
                for dy in (-0.4, 2.2):
                    for dz in (0, 1.0):
                        pts.append(Vector((cx + dx * Wm, cy + dy * Wm, root.location.z + dz * Wm)))
        xs = []; ys = []
        for p in pts:
            q = world_to_camera_view(scene, cam, p); xs.append(q.x); ys.append(q.y)
        x0, x1 = max(0, min(xs)), min(1, max(xs)); y0, y1 = max(0, min(ys)), min(1, max(ys))
        render_to(os.path.join(OUT, f'capa_{k}.png'), border=(x0, y0, x1, y1), transparent=True)
        bq = world_to_camera_view(scene, cam, Vector((cx, cy, ground_h(cx, cy))))
        meta[k] = dict(left=round(x0 * W), top=round((1 - y1) * H) - PAN, width=round((x1 - x0) * W), height=round((y1 - y0) * H),
                       ox=round(bq.x * W - x0 * W), oy=round((1 - bq.y) * H - (1 - y1) * H))
    json.dump(meta, open(os.path.join(OUT, 'capas.json'), 'w'), indent=1)
    print(meta)
