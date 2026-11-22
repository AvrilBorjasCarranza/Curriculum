"""Giro del pulpo para el anuncio. Blender 5.x (Scripting > New > pegar > Run Script).
Antes de ejecutar: selecciona TODAS las piezas del pulpo (cuerpo, ojos, labios, anillo) en el Outliner.
El script las agrupa bajo un Empty, las hace girar rápido al principio y lento al final, y deja listo el render
(CPU, pocas muestras + denoise, PNG con fondo transparente). Después: Render > Render Animation (Ctrl+F12)."""
import bpy, math
from mathutils import Vector

# ----- ajustes -----
VUELTAS   = 2        # vueltas completas (termina de frente)
FOTOGRAMAS = 48      # 2 s a 24 fps
RESOLUCION = 1000    # px (cuadrado)
MUESTRAS   = 48
SALIDA     = "//giro_pulpo/frame_"

partes = [o for o in bpy.context.selected_objects if o.type in {'MESH', 'CURVE', 'SURFACE', 'FONT'}]
if not partes:
    raise Exception("Selecciona todas las piezas del pulpo antes de ejecutar el script.")

scene = bpy.context.scene

# centro (x, y) y base (z) del conjunto de piezas
esquinas = [o.matrix_world @ Vector(c) for o in partes for c in o.bound_box]
minv = Vector((min(v.x for v in esquinas), min(v.y for v in esquinas), min(v.z for v in esquinas)))
maxv = Vector((max(v.x for v in esquinas), max(v.y for v in esquinas), max(v.z for v in esquinas)))
centro = Vector(((minv.x + maxv.x) / 2, (minv.y + maxv.y) / 2, (minv.z + maxv.z) / 2))

# Empty que gira sobre el eje vertical que pasa por el centro del pulpo
empty = bpy.data.objects.new("GiroPulpo", None)
empty.location = centro
scene.collection.objects.link(empty)
bpy.context.view_layer.update()
for o in partes:
    inversa = o.matrix_world.copy()
    o.parent = empty
    o.matrix_parent_inverse = empty.matrix_world.inverted()

# rotación: un fotograma clave por fotograma (funciona igual en todas las versiones)
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = FOTOGRAMAS
for f in range(1, FOTOGRAMAS + 1):
    t = (f - 1) / (FOTOGRAMAS - 1)
    suave = 1 - (1 - t) ** 3          # rápido al empezar, lento al terminar
    empty.rotation_euler = (0, 0, math.radians(360 * VUELTAS * suave))
    empty.keyframe_insert(data_path="rotation_euler", frame=f)

# render: CPU, pocas muestras, denoise, PNG transparente
r = scene.render
r.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = MUESTRAS
scene.cycles.use_denoising = True
try:
    scene.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception:
    pass
r.resolution_x = RESOLUCION
r.resolution_y = RESOLUCION
r.resolution_percentage = 100
r.film_transparent = True
r.image_settings.file_format = 'PNG'
r.image_settings.color_mode = 'RGBA'
r.image_settings.color_depth = '8'
r.filepath = SALIDA
scene.view_settings.view_transform = 'Standard'

print("Listo: pulsa Ctrl+F12 para renderizar", FOTOGRAMAS, "fotogramas en", SALIDA)
