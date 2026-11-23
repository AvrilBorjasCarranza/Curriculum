# Proyecto: mystery box de llaveros-pulpo (RenardLab3D)

Estado: concepto con decisiones tomadas (21/11/2026). Primero toca elegir el nombre de la serie.

## Idea
- Mystery box (caja sorpresa) de **llaveros** con forma de pulpo, impresos en 3D.
- Temática: **playa y mar**, porque son pulpos.
- Personaje principal / original: el **pulpo rosa** (modelo propio hecho en Blender, `concept/pulpo-rosa-blender.png`).
- Segundo personaje: pulpo **rojo enfadado**, con una vena de enfado.
- Vídeos: **revelar los pulpitos uno por uno**; el primero es el rosa, después el rojo enfadado.

## Paleta (de `concept/moodboard.png`)
| Nombre del moodboard | Color | Hex |
|---|---|---|
| 桃桃粉 (rosa melocotón) | rosa | `#FA96CD` |
| 海盐蓝 (azul sal marina) | azul claro | `#BAE6FD` |
| 芝士黄 (amarillo queso) | amarillo crema | `#FEF3C9` |

Fotos de ambiente: arena de playa con agua desenfocada y fondo marino turquesa con rayos de sol.

## Caja (referencia: caja «MINI HOLIDAY» del moodboard)
- **Nombre de la serie arriba.**
- **Personaje principal en el centro.**
- **A un lado, los personajes que pueden salir** (los secretos, como siluetas).
- **Fondo de la caja monocolor** (color por decidir).

## Texto
- «Style du texte 1»: letra gruesa, redondeada, con el trazo irregular.
- «Style du text 2»: letra cursiva fina, tipo pincel.
- El texto del moodboard está en francés: público francés.

## Decisiones tomadas (21/11/2026)
- **Serie: 5 diseños + 1 secreto = 6 pulpos.** Cada uno es de un color y tiene su personalidad:
  | Pulpo | Personalidad | Estado del modelo |
  |---|---|---|
  | Rosa (original, portada) | modelo base | hecho en Blender |
  | Rojo | enfadado, con una vena | hecho en Blender |
  | Amarillo | seguro de sí mismo, gafas de sol | por definir |
  | Azul | triste, llorando | por definir |
  | Verde | mareado, cara de querer vomitar | por definir |
  | Arcoíris (SECRETO) | saluda con un tentáculo arriba; único con cuerpo distinto al rosa | por definir |
- Fabricación: **impresión 3D en PLA**, piezas pegadas con pegamento (cuerpo, ojos, boca), **5 u 8 cm** de alto, con **cadena** (la anilla ya va impresa pegada al cuerpo en la última versión del modelo).
- **Primera prueba de impresión: 22/11/2026.** Apuntar gramos, tiempo y tamaño de cada pieza.
- **Caja:** fondo **azul liso**; nombre arriba (tipografía redondeada tipo burbuja); pulpo rosa en la portada; al lado los demás pulpos, y el secreto como **silueta negra con «?»**; incluye el **logo** (corregir antes «IMPRESION») y el porcentaje de probabilidad.
- **Un pulpo por bolsa.** Formato de caja por decidir: solo hay impresora de papel, así que hay que buscar una opción barata.
- Tipografías: una redondeada tipo burbuja (la que va en la caja) y otra delicada para contraste en la publicidad.
- Nombre de la serie: **«Octo...» gracioso o tierno** (en francés).

## Venta
- Dónde: Instagram, Vinted; estudian una web o catálogo.
- Precio previsto: **14,99 €** (a confirmar con su pareja tras los costes).
- Primera tirada: unas **18 cajas**, con **preventa** antes para medir la demanda.
- Público: gente que compra mystery boxes (Miniso, Pop Mart), coleccionistas y quien busca cosas tiernas.
- Misma cuenta de Instagram que el negocio (productos personalizados + productos propios).
- Envíos por toda Francia, paquete pequeño.

## Vídeos
- **Renders 3D** (giro de cada pulpo, de Blender).
- **Un pulpo por semana**, y en todos «preventa abierta».
- Sin voz: canción + efectos de sonido.
- Los pulpos aún no tienen nombre.

## Actualización (21/11/2026, tarde)
- **Nombre de la serie: finalistas OctoMood y OctoPlouf** (decidir; comprobar usuario de Instagram libre y la base de marcas del INPI, ojo con «Octonauts»).
- Los pulpos **se distinguen solo por color**: rosa, rojo, amarillo, azul, verde y arcoíris (secreto). Sin nombres de personaje.
- Se mantiene el lema «Quel est ton mood ?».
- **Envoltorio tipo caramelo**: rectángulo de papel pegado en cilindro, cerrado por arriba y por abajo con las solapas aplastadas y giradas 90° entre sí.
  - Medidas del boceto (A4 horizontal): rectángulo 235 × 170 mm = cuerpo 80 mm + dos solapas de 45 mm; ancho 220 mm (circunferencia) + 15 mm de pestaña; tubo de ≈ 7 cm de diámetro.
  - Cabe un pulpo de ≈ 5 cm (≈ 6 cm de ancho). **Un pulpo de 8 cm (≈ 9 cm de ancho) no cabe en una A4.**
  - Papel de 160–200 g. Hacer primero un prototipo con papel normal.
- **Probabilidad del secreto**: pendiente. Opciones: 20 unidades con 2 secretos (1 de 10, exacto) o 18 con 2 (1 de 9). La cifra impresa tiene que coincidir con el reparto real.
- Preventa por Instagram.
- Pendiente de ella: renders en PNG transparente de Blender (alta resolución) de cada pulpo, y las medidas reales tras la prueba de impresión del 22/11.
- Bocetos hechos: `diseno/envoltorio-plano.png`, `diseno/comparacion-nombres.png`, `diseno/personajes.png` (pulpos provisionales dibujados con código, generados por `diseno/gen_envoltorio.py`).

## Fondo
- **Azul liso y plano** (`#BAE6FD`): sin burbujas, degradados ni sombras en el fondo (decidido el 21/11/2026).
- Los renders reales de los pulpos se guardan en `diseno/pulpos/` (`rosa.png`, `rojo.png`, `amarillo.png`, `azul.png`, `verde.png`, `arcoiris.png`, PNG con fondo transparente). `gen_envoltorio.py` los usa en lugar de los dibujos provisionales.

## Colores y tipografía del envoltorio (21/11/2026)
- **Sin negro en el envoltorio**, salvo la silueta del pulpo secreto. Textos en azul profundo `#2A6FAE`; título en rosa `#FA96CD` con borde crema `#FEF3C9` y volumen en azul medio `#7FC2EC`.
- **Tipografía más «burbuja»**, una sola en la caja. Candidatas libres (Google Fonts, licencia OFL, uso comercial permitido): Modak, Bagel Fat One, DynaPuff y Titan One. Por defecto: **Bagel Fat One** (legible en tamaño pequeño). `FONT=Modak python3 gen_envoltorio.py .` cambia la fuente.
- Las fuentes del buscador de fuentes que enseñó (Bubble Bobble, Bubble Bash, Fluff Plush, Super Bubble…) suelen ser «solo uso personal»: antes de usar una para vender hay que comprobar la licencia.
- Pendiente: renders en PNG transparente y vídeo del giro de 360°.

## Tipografía y color de las letras (decisión final, 21/11/2026)
- **Título: Modak.** **Todo lo demás: Bagel Fat One.** Ambas libres (Google Fonts, OFL).
- **Todas las letras en amarillo `#FEF3C9`** con borde azul profundo `#2A6FAE` para que se lean sobre el azul `#BAE6FD`. El título lleva además una sombra rosa `#FA96CD`.
- Sigue sin haber negro en el envoltorio, salvo la silueta del pulpo secreto.

## Relieve de las letras (21/11/2026)
- Pedido: **solo relieve blanco**, sin azul ni rosa. Aplicado en `diseno/envoltorio-plano.png`.
- Problema: amarillo `#FEF3C9` + blanco + azul `#BAE6FD` son colores de luminosidad parecida y **el texto se lee muy mal**, sobre todo el pequeño (≈ 4 mm al imprimir).
- Prueba comparativa: `diseno/prueba-letras.png` (A fino, B más fino, C amarillo más intenso `#FFD84D`, D azul un poco más profundo `#7CCBF4`). **Recomendada: C.**
- Pendiente: que elija una opción para aplicarla a toda la hoja.

## Colores finales del envoltorio (21/11/2026, versión vigente)
- Pedido: **fondo claro, letras más oscuras y los 3 colores presentes** (rosa, azul, amarillo). El azul profundo `#2E8FD8` anterior se descartó.
- **Fondo amarillo liso `#FEF3C9`**; **título rosa oscuro `#C2377F`** (Modak); **resto del texto azul `#1F5F93`** (Bagel Fat One); etiqueta «SÉRIE 1» en **azul claro `#BAE6FD`**; pulpo central rosa `#FA96CD`.
- **Relieve solo blanco**, plano (sin burbujas ni degradados de fondo). Sin negro salvo la silueta del secreto (con «?» amarillo).
- Alternativas: B = fondo azul claro + etiqueta amarilla `#FFD84D`; C = fondo amarillo + título azul + etiqueta rosa. Variables: `BG`, `TT`, `TX`, `PILL`, `PILLTX`.
- Un fondo claro gasta mucha menos tinta que el azul sólido.

## Renders reales y siluetas (21/11/2026)
- `diseno/pulpos/rosa.png` ya es el render real de Blender (PNG transparente 2000 px, recortado). El color rosa del render se mantiene.
- En la contraportada, los pulpos **sin render real** se muestran como **silueta azul clara con «?» azul**; el secreto sigue en negro con «?» amarillo. Al guardar `rojo.png`, `amarillo.png`, `azul.png` o `verde.png` en `diseno/pulpos/`, la silueta se sustituye sola.

## Costes por pieza (21/11/2026, provisional)
- Datos del programa (1 pulpo, colores de prueba): 23,80 g (modelo 21,31 + soportes 1,71 + purga 0,78), 1 h 21 min, 2 cambios de filamento. Aviso: 9 zonas de voladizo sin soporte en CuerpoNormal.stl.
- Filamento: cuerpo 18,99 €/kg, ojos 20 €/kg, boca 18,98 €/kg → 0,45 €. Anilla 0,10 € (10 € / 100). Envoltorio 1,00 € (1 A4 = 1 envoltorio; 2 por hoja solo con tubo más pequeño). Pegamento ≈ 0,05 € (estimado).
- Trabajo a 12 €/h: diseño 45 min / 20 = 2,25 min; preparación 30 min por plato de 6 = 5 min; montaje de la caja 10 min → 3,45 €.
- Pérdida 10 %: 0,05 €. Cotizaciones ≈ 12,3 % (a verificar; aún no hay estatuto confirmado): 1,84 €. Pago por Revolut sin comisión; envío a cargo del comprador.
- Coste completo ≈ 6,97 €; precio mínimo ≈ 5,85 €; margen con 14,99 € ≈ 8,02 € por pieza (≈ 160 € con 20 cajas).
- Pendiente: plato real de 6–8 pulpos (mañana), pulpo secreto con filamento multicolor, estatuto de la empresa, coste de la impresora.
- Tabla en francés: `costes/prix.html` y `costes/prix.png`.
- Impresora Bambu A1: 339 €. Amortizada en ≈ 3 000 h (estimado) → 0,14 € por pieza. Coste completo ≈ 7,11 €, margen ≈ 7,88 €/pieza, precio mínimo ≈ 6,01 €. Se recupera con ≈ 30 piezas vendidas sin contar el sueldo (≈ 43 contándolo).
- Respuestas de Enzo (21/11): plato de 6–8 lo hará otro día; preparación 30 min por plato; montaje «≈ 40 min» (Avril dijo 10: por aclarar); tarifa 14 €/h (SMIC luxemburgués); sin estatuto ni empresa; venta en Vinted o Leboncoin; envío a cargo del comprador; A1 de Bambu Lab, kWh ≈ 0,20 €; pulpo secreto = filamento especial más caro; barra de pegamento: >20 platos sin acabarla; fallos 10 %.
- Cálculo con 14 €/h, montaje 10 min, sin cotizaciones: coste completo ≈ 5,85 €, margen ≈ 9,14 €/pieza (≈ 183 € con 20 cajas); con montaje de 40 min el margen baja a ≈ 2,14 €.

## Cambio: el pulpo principal pasa de rosa a morado (22/11/2026)
- La portada y los archivos usan ahora `diseno/pulpos/morado.png` (render de Blender, cuerpo morado, ojos negros, labios rosa-rojo). `rosa.png` desaparece.
- Serie actual: **morado**, rojo, amarillo, azul, verde + secreto arcoíris. En el generador, `PURP` sustituye a `PINKO`.
- Morado y rojo comparten el mismo recorte cuadrado (277,285 → 1711,1719 del render de 2000 px) para conservar la escala entre ellos.
- Los colores del envoltorio (fondo amarillo, título rosa oscuro, texto azul) no cambian.
- Color del morado (22/11): objetivo medido en las fotos del pulpo impreso = RGB(131, 99, 216) / #8363D8. Los renders de Blender salían más oscuros (≈ #685AAE) aunque se cambió el Hex y la exposición, así que se corrigió el render por post-proceso (ganancia lineal por canal sólo en el cuerpo, sin tocar ojos ni labios). `pulpos/morado.png` queda en #8362D7; `morado_original_2000.png` guarda el PNG corregido completo.
- Pendiente en Blender: que la exposición y el color base se apliquen de verdad (comprobar View Transform = Standard, Exposure y el material correcto del cuerpo) para que los demás renders salgan ya bien.

## Anuncio 3D (idea, 22/11/2026)
- Guion: pulpo morado gira sobre cielo azul claro (#BAE6FD) → cae a la playa (arena #FEF3C9) con las 5 siluetas «?» detrás → aparece «OctoMood» (Octo en coral como el pulpo rosa original ≈ #D9606A; Mood en azul, relieve blanco, tipografía Modak) → logo en la esquina de arriba (zona segura). ≈ 6 s.
- Reparto: Blender sólo renderiza el giro (≈ 36–48 fotogramas, PNG transparente ≈ 1000×1000, CPU con denoise); la caída, siluetas, texto, logo y música se montan en HyperFrames.
- Contraste: el azul exacto de la paleta (#BAE6FD) no se lee con relieve blanco ni sobre cielo ni sobre arena; comparativa en `video3d/titulo.png`.

## Decisiones del anuncio 3D (22/11/2026)
- Título: Octo en coral y Mood en azul `#8DD0F7`, relieve blanco, Modak. Logo corregido a «IMPRESSION 3D» (`logo/logo-renardlab-impression.png`, fondo transparente).
- Precio: 14,99 € tachado con animación → «Prix de lancement 12,99 €». Preventa hasta el 20 de enero (2027), «20 pièces seulement». Pedidos por DM (@renardlab3d). Sin sonido de tendencia ni voz.
- Siluetas del vídeo: amarillas con «?» (4) y una negra (secreto), para contrastar con cielo y arena.
- Fondo: escena 3D (cielo + playa con sombras y textura) que renderiza Avril como imagen; la caída del pulpo cambia del render 3D a la foto de la pieza real sobre el mismo fondo.
- Giro: rápido al empezar y lento al final (`video3d/giro_pulpo.py`, sin probar en Blender; Avril pasa el Outliner mañana).
- Música: opciones en `musica-opciones/` (las CC BY exigen crédito).

## Borrador del anuncio (22/11/2026) — `reel-3d/`
- Música elegida: jingle C original (`musica-opciones/jingle_C_banda_120bpm.mp3`, 10 s, 120 BPM).
- Borrador renderizado: `reel-3d/renders/octomood-borrador.mp4` (10 s, 1080×1920, −13,5 LUFS). Generador: `reel-3d/tools/gen_3d.py`.
- Piezas provisionales que sustituirá Avril: fondo (cielo + playa) → render de Blender; giro → fotogramas de Blender (ahora es un giro falso con scaleX); «pieza real» → `reel-3d/assets/pieza-real.png` (si existe, el generador cambia el 3D por la foto al aterrizar).
- Sonidos (del banco local): pop (aparición, siluetas, título, pancarta), whoosh (caída y cambio de plano), impacto grave (aterrizaje), clic (tachado), destello (precio y final).
- `check` señala contraste bajo en «Mood» (#8DD0F7, 1,3:1): decisión de Avril; se lee por el relieve blanco. Opción más legible: #5BB5EE.

## Rosa de marca = coral de Octo (22/11/2026)
- Todo el rosa de la marca pasa a ser el coral del pulpo original: **#CD575B** (título «OctoMood» del envoltorio, pancarta, precio y tachado del vídeo). Se abandonan #C2377F y #FA96CD.
- Anuncio 3D: fondo (cielo, mar, arena con relieve irregular y sol/nubes), siluetas amarillas 3D y secreto negro se renderizan en Blender 5.1.2 con `reel-3d/tools/escena_playa.py` (módulo `bpy`, CPU, ≈ 5 min a resolución completa) y `tools/pulir_capas.py`. Distribución: morado delante, 2 amarillas a cada lado en forma de triángulo y la negra detrás en la arena. Render: `reel-3d/renders/octomood-3d.mp4`.

## Ajustes del anuncio y del paquete (22/11/2026, 2.ª ronda)
- Mar 3D con oleaje irregular (malla con olas largas y rizado, color turquesa→azul, espuma ondulada en la orilla); cámara a 2,4 m, orilla a 30 m.
- Todos los pulpos subidos; sombra del morado suavizada (alfa × 0,38 y sol más difuso).
- Siluetas amarillas y negra = contorno del pulpo real (máscara `reel-3d/assets/sil_mask.png`, inflada en 3D). En el paquete se usan `diseno/pulpos/sil_azul.png` y `sil_negra.png`.
- Título del paquete = título del vídeo (Octo coral #CD575B + Mood #8DD0F7, Modak, relieve blanco).
- Siluetas del anuncio rehechas como el modelo original: cuerpo de revolución con «pelotas» que se funden (metaballs): cabeza + 8 pelotitas-brazo en anillo + anilla; más pequeñas. Orilla del mar suavizada (agua transparente en la orilla, arena húmeda, espuma difusa y curva irregular).
- Música «de burbuja»: `musica-opciones/jingle_E_burbujas_108bpm.mp3` y `jingle_F_burbujas_blops_108bpm.mp3` (generador `generar_burbujas.py`). Pendiente de que Avril elija.
- Música elegida: H1 (marimba) y H3 (ukelele), ambas con pops de burbuja y sin agudos. Vídeos: `reel-3d/renders/octomood-3d-H1.mp4` y `octomood-3d-H3.mp4` (−13,8 y −13,5 LUFS). Pendiente: que Avril elija una.
- **Música definitiva del anuncio: H3 (ukelele + pops de burbuja, 108 BPM, generada por código, sin licencias ni crédito).** Vídeo: `reel-3d/renders/octomood-3d.mp4`. Pops de burbuja en los textos del final.

## Anuncio con el modelo real (22/11/2026)
- Modelo STL de Avril (`reel-3d/assets/modelo/OctoSmoot.stl`, 7 piezas: cuerpo, 2 ojos, boca ×2, anilla ×2) colocado en la playa 3D. Giro (rápido→lento), caída, aplastamiento y rebote renderizados en Blender (`tools/anim_pulpo.py`, 94 fotogramas, WebM con alfa) con sombra real. Color del cuerpo calibrado para que el render dé ≈ (131, 99, 216), como la pieza impresa (base en Blender #7051C4).
- Las 4 siluetas amarillas y la negra usan el mismo STL (cuerpo + anilla) en color plano y «?»; paquete: contorno de frente del STL (`reel-3d/assets/sil_mask.png`).
- Vídeo final: `reel-3d/renders/octomood-3d.mp4` (música H3, 10 s, −13,6 LUFS).
- **Cámara en movimiento (22/11/2026):** a la altura del pulpo (algo más cerca) durante el giro; baja con él al caer; al aterrizar se abre hacia atrás y arriba y aparecen las siluetas. Escena completa renderizada en Blender (`reel-3d/tools/anim_camara.py`, 57 + 64 fotogramas; `montar_camara.sh` los codifica). Vídeo: `reel-3d/renders/octomood-3d-camara.mp4` (= `octomood-3d.mp4`).
- Sonidos: 7 pops de burbuja (la mitad que antes), hush al caer más fuerte, pop grave al aterrizar. Precio: más espacio entre «PRIX DE LANCEMENT» y 12,99 €.
- **Apertura solo cielo (22/11/2026):** el horizonte empieza fuera de cuadro (desplazamiento de lente) y sube a cuadro durante la caída; el pulpo queda ≈ 14° por encima de la cámara en el giro (no se puede ver solo cielo y a la vez a la altura exacta de sus ojos). Vídeo: `reel-3d/renders/octomood-3d-camara.mp4`.
- Combinaciones de color del vídeo del nacimiento = las de las fotos de Blender de Avril: rosa (cuerpo #F2A0C8, boca #D95B94), lavanda (cuerpo #6F7BE6, boca #F08FA6), lavanda de un solo color, y el violeta final (#7051C4 + boca coral). Sin rojo. Boca (3,4 s) y anilla (4,7 s) separadas con su propio texto. 11,6 s.
- Vídeo del nacimiento, 2.ª versión (23/11): sin bolitas sueltas (falsas); una bola rosa → cuerpo completo → ojos → boca → anilla (todo ya en color rosa) → lavanda → todo lavanda → violeta. 10 s, 8 pops con gotitas blancas.
- Vídeo del nacimiento, 3.ª versión (23/11): todo blanco primero (bola → cuerpo → boca → anilla, sin ojos); después 4 colores rápidos sobre cuerpo, labios y anilla (rosa, lavanda/coral, lavanda mono, violeta) y al final los ojos negros. 10 s. `reel-proceso/renders/nacimiento-octo.mp4`.
- Vídeo del nacimiento, 4.ª versión (23/11): estructura blanca (bola, cuerpo, boca, anilla) → el CUERPO prueba 4 colores (rosa, lavanda, lila, violeta) con la boca blanca → el cuerpo se queda violeta y los LABIOS prueban 4 colores (rosa, lavanda, melocotón, coral) → ojos negros al final. 12,2 s.
