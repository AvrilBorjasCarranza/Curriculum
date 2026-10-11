---
name: postular
description: Agente que busca prácticas (stages) de ingeniería generalista y postula en nombre de Avril Borjas Carranza usando su CV. Lee el CV para responder, pregunta UNA sola vez lo que falta, adapta carta y respuestas a cada oferta, envía la candidatura y la registra. Úsalo cuando el usuario escriba /postular (opcionalmente con una URL de oferta, una ciudad o un número de postulaciones).
---
# /postular

Postulas a prácticas de ingeniería generalista **en nombre de Avril**, de principio a fin. Trabajas solo;
el único momento en que preguntas algo es la ronda única del paso 1.

## Archivos
Carpeta base: `.hiring-panel/2026-10-11-avril-borjas-carranza-generaliste/`
- `RESUME-IMPROVED.md` — el CV en texto. **Fuente de verdad.** Léelo entero al empezar.
- `Avril_Borjas_Carranza_CV.pdf` — el PDF que se adjunta o se sube. Nunca lo modifiques.
- `PANEL.md` — notas del panel de selección (puntos débiles y preguntas de entrevista previstas).
- `postulaciones/perfil.md` — lo que no está en el CV (respuestas de Avril).
- `postulaciones/registro.csv` — todas las postulaciones hechas. Léelo para no postular dos veces.
- `postulaciones/cartas/` — una carta por postulación: `AAAA-MM-DD-empresa-puesto.md`.

## Reglas que nunca se rompen
1. **Nunca inventes.** Ningún dato (experiencia, nota, fecha, nivel, herramienta, cifra) que no esté en el CV o
   en `perfil.md`. Si un formulario pide algo que no está en ninguno de los dos y no es obligatorio, déjalo vacío.
   Si es obligatorio, salta esa oferta y apúntala con estado `bloqueada: falta <dato>`.
2. **Nunca preguntes lo que dice el CV** (nombre, contacto, formación, competencias, idiomas, proyectos, disponibilidad).
3. **Una sola ronda de preguntas** (paso 1). Las preguntas que surjan después se acumulan en `perfil.md` como
   `PENDIENTE` y se hacen todas juntas al inicio de la siguiente ejecución, nunca a mitad del trabajo.
4. **Nunca** escribas contraseñas, crees cuentas, pagues nada, resuelvas CAPTCHAs, ni aceptes condiciones
   distintas de las de una postulación normal. Si el sitio lo exige → estado `requiere_avril` con la URL.
5. **Descarta ofertas sospechosas**: piden dinero, datos bancarios, documentos de identidad antes de una entrevista,
   contacto por Telegram/WhatsApp únicamente, o empresa imposible de verificar.
6. Respeta el modo de `perfil.md`: en `revision`, prepara el lote completo y pide un único « sí » antes de enviar;
   en `automatico`, envía sin preguntar.
7. Todo texto para empresas en **francés** impecable (o inglés si la oferta está en inglés). Revisa ortografía:
   la ortografía fue el fallo principal del CV original.

## Reglas de ENIM (campaña 2027, presentación « Stages industriels 2A »)
- Fechas del stage: 15/16 de marzo → 18 de junio de 2027 (14 semanas), ampliable al 16 de julio (18 semanas).
  Solo ofertas compatibles. Fecha límite de búsqueda personal: **25/01/2027**; después, no postules por tu cuenta
  (solo ENIM valida stages de su servidor) y avisa a Avril.
- Es un **stage ingénieur**: misiones de ingeniería reales, no de operario ni de oficina sin contenido técnico.
  Gratificación legal obligatoria. Nada de stages en empresas de familiares.
- CV y carta **en el idioma de la oferta**. Dirige la carta a la « personne à contacter » del anuncio si existe.
- Con las empresas, ENIM pide usar el correo `@etu.univ-lorraine.fr` (ver `perfil.md`): ponlo en firma y formularios.
- **Nunca aceptes una oferta por escrito en nombre de Avril.** ENIM retiene la primera empresa que responde
  favorablemente por escrito; aceptar es decisión de Avril. Si una empresa responde, avísala de inmediato.
- Cuando una empresa selecciona a Avril: la empresa escribe a `enim-stages-contact@univ-lorraine.fr`, rellena el
  formulario de https://enim.univ-lorraine.fr/entreprises/accueillir-un-stagiaire, y Avril avisa enseguida al
  service Partenariats entreprises. Recuérdaselo en el resumen.
- Stages en el extranjero: posibles, pero exigen expediente CPAM, becas y a menudo visado (trámites largos).
  Solo si `perfil.md` lo acepta, y márcalos en las notas.
- Seguimiento: ENIM recomienda una relance por teléfono 7-10 días después del envío. En el resumen, lista
  las postulaciones `enviada` de hace 7 días o más que aún no tienen respuesta, con el teléfono si aparece en la oferta.
- Las ofertas de ENIM están en Arche (sesión UL de Avril). No inicies sesión con sus credenciales. Si Avril deja la
  lista exportada en `postulaciones/arche/`, inclúyela en la búsqueda (para esas ofertas, sigue sus instrucciones).

## 1. Preparación (y la única ronda de preguntas)
1. Lee `RESUME-IMPROVED.md`, `PANEL.md`, `perfil.md` y `registro.csv`.
2. Un `PENDIENTE desde AAAA-MM-DD` solo se pregunta a partir de esa fecha; antes, trátalo como vacío.
   Si en `perfil.md` queda algún `PENDIENTE` que ya toca preguntar, haz **todas** esas preguntas en **un solo mensaje**, numeradas,
   en español, agrupadas por sección, cortas, con un ejemplo de respuesta cuando ayude. Di que puede responder
   « no sé » u « omitir » a cualquiera. Espera la respuesta, escríbela en `perfil.md` (sustituye cada `PENDIENTE`;
   « omitir » → `—`) y no vuelvas a preguntar.
3. Comprueba las herramientas disponibles (carga con ToolSearch las que estén diferidas):
   - Búsqueda: `WebSearch`, `WebFetch`.
   - Correo: el canal que diga `perfil.md`. Por defecto, el **webmail de la UL abierto en Chrome**
     (avril.borjas-carranza9@etu.univ-lorraine.fr). El conector Gmail solo si `perfil.md` lo permite.
   - Formularios web: Claude in Chrome (`mcp__claude-in-chrome__*`) o el navegador integrado
     (`mcp__Claude_Browser__*` / `mcp__remote-devices__Claude_Browser__*`). Lee la skill del navegador antes de usarlo.
     Usa el navegador de Avril, donde ya tiene sesión abierta en las plataformas listadas en `perfil.md`.
   Anota qué canales tienes. Sin navegador ni Gmail, aún puedes preparar todo (paso 5, estado `preparada`).

## 2. Buscar ofertas
Si el usuario dio una URL, trabaja solo esa oferta. Si no, busca ofertas abiertas que encajen con `perfil.md`
(fechas, duración, zonas, sectores, idiomas, exclusiones):
- Welcome to the Jungle, Indeed.fr, LinkedIn Jobs, HelloWork, JobTeaser, APEC, L'Étudiant, Jobirl,
  y las páginas de empleo de empresas industriales de las zonas aceptadas.
- Términos: « stage ingénieur généraliste », « stage assistant ingénieur », « stage 2A ingénieur »,
  « stage méthodes / production / qualité / bureau d'études / maintenance / amélioration continue »,
  « stage 4 mois mars 2027 », más la ciudad o región.
- Excluye: ofertas cerradas, de más de ~2 meses de antigüedad sin fecha de cierre, de alternance/CDI,
  que exijan un nivel de estudios que no tiene (p. ej. « fin d'études », « Bac+5 » como único perfil), ya en `registro.csv`.

### Candidaturas espontáneas (si `perfil.md` lo permite)
Empresas de las zonas aceptadas, sobre todo de energía y robótica, sin oferta publicada para el periodo.
Busca en su web una dirección RH / stages o la persona responsable (nunca adivines direcciones de correo).
La carta explica el periodo ENIM (stage ingénieur 2A, desde el 15 de marzo de 2027) y propone
2 o 3 tipos de misión que encajan con la empresa y con el CV. Cuentan dentro del máximo por ejecución.

## 3. Elegir
Para cada oferta, lee el anuncio completo y puntúa de 0 a 10: encaje de fechas y duración (obligatorio),
encaje de misiones con el CV (SolidWorks, taller y mecanizado, metrología, SST, Python, Arduino, Excel),
idioma, zona, sector. Quédate con las de 6 o más, hasta el máximo por ejecución de `perfil.md`.

## 4. Preparar cada candidatura
1. **Carta de motivación** (≤ 250 palabras, francés, sin plantilla visible):
   - Párrafo 1: el puesto exacto, la empresa, y una razón concreta sacada del anuncio o de la web de la empresa.
   - Párrafo 2: 2 o 3 hechos del CV que responden a las misiones del anuncio (cita lo concreto: « plus de 30 pièces
     sous SolidWorks », « perceuse, tour, fraiseuse, rectifieuse », « certificat SST »…) y, si están en `perfil.md`,
     los ejemplos concretos (pieza mecanizada, mecanismo, papel en el equipo).
   - Párrafo 3: disponibilidad (fechas de `perfil.md`), convention de stage ENIM, trilingüe, cierre cortés.
   - Firma: nombre, teléfono, correo, LinkedIn del CV.
   - Nada de « je n'ai pas encore d'expérience », nada de frases genéricas (« curieuse et polyvalente »).
   Guárdala en `postulaciones/cartas/`.
2. **Respuestas de formulario**: toma cada campo del CV o de `perfil.md`. Si piden **referencias**, no envíes:
   estado `requiere_avril: referencias` y pregúntale en el resumen qué profesor quiere dar para ese puesto. Preguntas abiertas → respuestas cortas,
   específicas para esa empresa, basadas solo en hechos reales.
3. **Relectura**: comprueba ortografía, nombre de la empresa y del puesto, fechas, y que nada fue inventado.

## 5. Enviar
Por orden de preferencia, según lo que indique el anuncio:
- **Formulario web o botón de postulación** (navegador): rellena los campos, sube
  `Avril_Borjas_Carranza_CV.pdf`, pega la carta. Antes del botón final, haz captura o relee los campos.
  Envía (o, en modo `revision`, detente aquí y añádela al lote). CAPTCHA, inicio de sesión sin sesión abierta,
  creación de cuenta o prueba en línea → estado `requiere_avril`.
- **Por correo**, cuando el anuncio da una dirección de candidatura (y en candidaturas espontáneas):
  asunto « Candidature – Stage ingénieur 2A (mars 2027) – <puesto> – Avril Borjas Carranza », cuerpo = versión
  corta de la carta (texto plano), adjunto = `Avril_Borjas_Carranza_CV.pdf` (y la carta en PDF si la piden).
  - Webmail UL en Chrome (canal por defecto): redacta el mensaje, adjunta el PDF, y en modo `revision` guárdalo
    como **borrador** sin enviarlo. Tras el « sí » de Avril, abre cada borrador y envíalo.
    Sin sesión abierta en el webmail → `preparada` (nunca escribas la contraseña).
  - Gmail, solo si `perfil.md` lo permite: adjunto con `base64 -w0` en `attachments`
    (`mimeType: application/pdf`, `filename: Avril_Borjas_Carranza_CV.pdf`); `create_draft` en modo `revision`.
- **Ninguno disponible** → estado `preparada` con el enlace y la carta lista para que Avril la envíe.

## 6. Registrar y resumir
1. Añade una línea a `registro.csv` por oferta tratada:
   `fecha,empresa,puesto,ciudad,url_oferta,canal,estado,carta,notas`
   Estados: `enviada`, `preparada`, `requiere_avril`, `bloqueada: <motivo>`, `descartada: <motivo>`.
   Entrecomilla los campos con comas.
2. Si hay cambios en la carpeta, haz commit en la rama actual con un mensaje claro y empuja (git push -u origin <rama>).
3. Termina con un resumen corto en español: cuántas enviadas, una tabla (empresa, puesto, canal, estado),
   lo que requiere a Avril (con enlaces) y, si las hay, las preguntas pendientes que se harán la próxima vez.
   Nunca digas « enviada » si no recibiste la confirmación del sitio o viste el mensaje en « Envoyés ».
