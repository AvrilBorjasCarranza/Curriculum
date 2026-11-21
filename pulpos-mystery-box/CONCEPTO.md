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

## Colores finales del envoltorio (21/11/2026, decididos «de forma óptima»)
- **Fondo azul liso `#2E8FD8`** (más profundo que el pastel `#BAE6FD`, que no daba contraste suficiente).
- **Letras amarillo `#FFD84D` con relieve blanco** (título: Modak; resto: Bagel Fat One). Etiqueta «SÉRIE 1»: rosa `#FA96CD` con letras amarillas.
- Pulpo rosa en el centro (resalta sobre el azul). Sin negro, salvo la silueta del secreto (con el «?» en amarillo).
- Se genera con `diseno/gen_envoltorio.py`. Variables: `BG` (fondo) y `YEL` (amarillo de las letras).
- Aviso de impresión: un fondo azul sólido gasta bastante tinta (≈ 64 % de la A4 por hoja) y puede salir con bandas en una impresora doméstica. Probar con papel mate de 160–200 g y calidad alta antes de la tirada.
