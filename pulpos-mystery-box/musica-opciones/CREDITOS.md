# Opciones de música (previews de 16 s) — licencias a confirmar en la fuente antes de usar

| Archivo | Título | Autor | Licencia (según Openverse) | Estilo |
|---|---|---|---|---|
| opcion_ukulele_chill.mp3 | Ukulele_Chill | larsn.wav | CC0 (sin crédito) | ukulele tranquilo |
| opcion_blue_sky.mp3 | Blue Sky | Sergmusic | CC0 (sin crédito) | alegre, luminoso |
| opcion_weekend_days.mp3 | Weekend Days (Cut Version) | UNIVERSFIELD | CC BY (crédito obligatorio) | pop suave corto |
| opcion_dreams_good_times.mp3 | Dreams Of Good Times | UNIVERSFIELD | CC BY (crédito obligatorio) | pop alegre |
| opcion_stagepop.mp3 | Stagepop | kjartan_abel | CC BY (crédito obligatorio) | pop animado |
| opcion_le_surfuku.mp3 | Le Surfuku | Léo Lago | CC BY (crédito obligatorio) | surf alegre |
| opcion_power_pop.mp3 | Super Power Pop Rock | Kara Square | CC BY (crédito obligatorio) | pop rock enérgico |

Las pistas CC BY exigen poner el crédito (título, autor y licencia) en la descripción del vídeo. Las CC0 no.

## Jingles propios (sin licencias de terceros)
- `jingle_A_campanitas_126bpm.mp3` — campanitas «tin tin tirin» + bajo, bombo suave, palmas y shaker; Do mayor, 126 BPM, 10 s, −15,5 LUFS.
- `jingle_B_ukulele_132bpm.mp3` — rasgueos tipo ukulele + campanitas más rápidas; Do mayor, 132 BPM, 10 s, −15,7 LUFS.
- Generados con `generar_jingles.py` (numpy, sin dependencias externas). No se han «escuchado»: sólo medidos (volumen y pico).
- `jingle_C_banda_120bpm.mp3` — banda completa a 120 BPM: campanitas (con doblado de octava), ukulele rasgueado, pad, bajo con ritmo, batería, arpegio de marimba, riser y golpe final; −15,5 LUFS.
- `jingle_D_silbido_120bpm.mp3` — igual que C, pero con la melodía doblada por un silbido en lugar del doblado de campanitas; −15,6 LUFS.
- Generados con `generar_jingles_v2.py`.
- Variaciones de C (`generar_jingles_v3.py`, la C original no se toca):
  - `jingle_C1_brillante_120bpm.mp3` — más agudos (destello de campanitas agudas en semicorcheas, hi-hats más claros, menos bajo y bombo, realce de agudos); agudos 17 %.
  - `jingle_C2_saltarina_120bpm.mp3` — swing en las corcheas, bajo corto y saltarín, palmas dobladas, marimba y ukulele más presentes.
  - `jingle_C3_playa_120bpm.mp3` — aire de playa: congas, melodía doblada con timbal metálico tipo steel drum, ukulele más fuerte, pad más bajo.
- Música de burbuja (`generar_burbujas.py`, `generar_burbujas_v2.py`): E (108 BPM, elegida), F (con blops), y variaciones de E: E1 caja de música 118 BPM (melodía una octava arriba, celesta, arpegio), E2 blub suave 100 BPM (burbujas con glissando, swing, bajo más presente), E3 cristal 112 BPM (destellos de cristal y arpegio). Todas ≈ −15 LUFS.
