# Graph Report - Curriculum  (2026-11-19)

## Corpus Check
- Corpus is ~34,862 words - fits in a single context window. You may not need a graph.

## Summary
- 204 nodes · 304 edges · 17 communities (15 shown, 2 thin omitted)
- Extraction: 85% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 44 edges (avg confidence: 0.86)
- Token cost: 270,984 input · 0 output

## Community Hubs (Navigation)
- Reel Generators (Python)
- Short Reel Composition
- Voice Editing Tool
- Credits and Sound Review
- Hook Products Christmas Scenes
- Long Reel Config
- Short Reel Config
- Brand Printer Map Scenes
- Short Reel npm Scripts
- Word Captions System
- Collaboration Exclusivity Scenes
- Long Reel npm Scripts
- HyperFrames Project Rules
- DM and Share Ending
- Snow Overlay
- Whip Pan Transition
- Guide Media Loader

## God Nodes (most connected - your core abstractions)
1. `Main Reel Composition (RenardLab3D, 50.076s portrait)` - 17 edges
2. `window.__timelines registry` - 16 edges
3. `scene_file()` - 13 edges
4. `Main composition (reel court, 18.32 s, 1080x1920)` - 10 edges
5. `Snow Ambient Overlay` - 9 edges
6. `RenardLab3D reel credits` - 9 edges
7. `Captions Composition (word-timed French captions)` - 8 edges
8. `Whip Pan Cut Transition Component` - 7 edges
9. `Main GSAP timeline (window.__timelines['main'])` - 7 edges
10. `earshot critique of renardlab3d-reel-final.mp4 (launch-grade, 21/23)` - 7 edges

## Surprising Connections (you probably didn't know these)
- `HyperFrames Composition Project (reel-court)` --semantically_similar_to--> `HyperFrames Composition Project (reel-renardlab)`  [INFERRED] [semantically similar]
  reel-court/AGENTS.md → reel-renardlab/AGENTS.md
- `Music track music.mp3 (volume 0.18)` --references--> `"Hip-Hop Jazz" by Prospect Of Idiots (CC BY 3.0, Jamendo)`  [AMBIGUOUS]
  reel-court/index.html → reel-renardlab/CREDITS.md
- `SUBS subtitle timings` --semantically_similar_to--> `Captions sub-composition (word-level karaoke captions)`  [INFERRED] [semantically similar]
  reel-renardlab/guia-rodaje/guia-rodaje.html → reel-court/compositions/captions.html
- `S6 Exclu Scene (exclusivity)` --semantically_similar_to--> `blurIn Stage Transition (opacity+blur+scale)`  [INFERRED] [semantically similar]
  reel-renardlab/compositions/s6-exclu.html → reel-renardlab/compositions/s4-produits.html
- `End card: logo, IMPRESSION 3D PERSONNALISÉE · METZ, ÉCRIS-NOUS EN DM` --references--> `Logo RenardLab Impression 3D`  [INFERRED]
  reel-court/index.html → reel-renardlab/CREDITS.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **RenardLab Reel Scene Sequence (S1-S11)** — reel_renardlab_compositions_s1_hook_hookscene, reel_renardlab_compositions_s2_reste_restescene, reel_renardlab_compositions_s3_marque_marquescene, reel_renardlab_compositions_s4_produits_produitsscene, reel_renardlab_compositions_s5_ensemble_ensemblescene, reel_renardlab_compositions_s6_exclu_excluscene, reel_renardlab_compositions_s7_facile_facilescene, reel_renardlab_compositions_s8_noel_noelscene, reel_renardlab_compositions_s9_france_francescene, reel_renardlab_compositions_s10_dm_dmscene, reel_renardlab_compositions_s11_partage_partagescene, reel_renardlab_index_main_composition [EXTRACTED 1.00]
- **Hand-rolled Whip Pan Transitions Between Scenes** — reel_renardlab_compositions_s1_hook_whipout, reel_renardlab_compositions_s2_reste_whipin, reel_renardlab_compositions_s1_hook_hookscene, reel_renardlab_compositions_s2_reste_restescene, reel_renardlab_compositions_s4_produits_produitsscene, reel_renardlab_compositions_s5_ensemble_ensemblescene, reel_renardlab_compositions_s8_noel_noelscene, reel_renardlab_compositions_s9_france_francescene [INFERRED 0.85]
- **Position-Matched Zoom/Reveal Transitions** — reel_renardlab_compositions_s2_reste_orange_flood, reel_renardlab_compositions_s3_marque_object_zoom_out, reel_renardlab_compositions_s7_facile_clip_circle_reveal, reel_renardlab_compositions_s9_france_pin_zoom_transition, reel_renardlab_compositions_s11_partage_clip_circle_reveal [INFERRED 0.85]
- **RenardLab reel sound pipeline: real-sfx placement, earshot verification, credited libraries** — reel_renardlab_credits_real_sfx_skill, reel_renardlab_credits_earshot, reel_renardlab_docs_real_sfx_critique_critique_round_1, reel_renardlab_docs_earshot_critique_earshot_critique, reel_renardlab_sfx_library_credits_credits, reel_renardlab_sfx_library_earshot_credits_credits [INFERRED 0.85]
- **Reel court timed layers on the main timeline** — reel_court_index_main, reel_court_index_main_timeline, reel_court_compositions_captions_captions, reel_court_index_voice, reel_court_index_music, reel_court_index_broll_clips [EXTRACTED 1.00]

## Communities (17 total, 2 thin omitted)

### Community 0 - "Reel Generators (Python)"
Cohesion: 0.10
Nodes (21): align(), norm(), align(), bulb(), norm(), prelude_for(), proj(), s1() (+13 more)

### Community 1 - "Short Reel Composition"
Cohesion: 0.13
Nodes (21): Captions sub-composition (word-level karaoke captions), Captions GSAP timeline (window.__timelines['captions']), Emphasised caption words (COPIE, RENARDLAB3D, PERSONNALISÉS, MASCOTTE, CONCURRENT, DM), window.__hyperframes.fitTextFontSize, Pieuvre Blender model card (MODÈLE 3D · CRÉÉ POUR TOI), B-roll clips c1–c6 (ours plateau, timelapse, impression, personnages, exclusif), Captions sub-composition slot, End card: logo, IMPRESSION 3D PERSONNALISÉE · METZ, ÉCRIS-NOUS EN DM (+13 more)

### Community 2 - "Voice Editing Tool"
Cohesion: 0.22
Nodes (11): add_pauses(), cut(), env_db(), fade(), quietest(), refine_end(), refine_start(), remove_breaths() (+3 more)

### Community 3 - "Credits and Sound Review"
Cohesion: 0.14
Nodes (17): RenardLab3D reel credits, earshot (Leonxlnx/earshot), "Hip-Hop Jazz" by Prospect Of Idiots (CC BY 3.0, Jamendo), Logo RenardLab Impression 3D, Pixabay SFX (Pixabay Content License, via media-use), real-sfx skill (Clipwing/skills), "Sleigh bells" Wikimedia Commons CC0, earshot critique of renardlab3d-reel-final.mp4 (launch-grade, 21/23) (+9 more)

### Community 4 - "Hook Products Christmas Scenes"
Cohesion: 0.19
Nodes (12): fireSfx() hf:sfx CustomEvent (whip-cut), COPIE! Stamp + Shop Shake, S1 Hook Scene (copied idea), Idea Bulbs (TOI vs EN FACE), Three Product Beats (figurine, porte-cles, personnages), S4 Produits Scene (figurine, keychain, characters), S8 Noel Scene (Christmas), Christmas Ornaments + Gift Box (+4 more)

### Community 5 - "Long Reel Config"
Cohesion: 0.18
Nodes (10): authoringSkill, media, autoProxy, paths, assets, blocks, components, registry (+2 more)

### Community 6 - "Short Reel Config"
Cohesion: 0.20
Nodes (9): authoringSkill, media, autoProxy, paths, assets, blocks, components, registry (+1 more)

### Community 7 - "Brand Printer Map Scenes"
Cohesion: 0.22
Nodes (6): S2 Reste Scene (stay open), 3D Printer Layer-by-Layer Build (gantry + head + 16 layers), RenardLab3D Logo + Letter Stagger Reveal, S3 Marque Scene (RenardLab3D brand + 3D print), France Map Delivery Routes from Metz, S9 France Scene (Metz + delivery)

### Community 8 - "Short Reel npm Scripts"
Cohesion: 0.22
Nodes (8): name, private, scripts, check, dev, publish, render, type

### Community 9 - "Word Captions System"
Cohesion: 0.28
Nodes (8): Captions Composition (word-timed French captions), Emphasized Caption Words (.emph yellow, overshoot scale), fitTextFontSize Auto-Sizing (58-92px), Caption Word Pop Animation (back.out scale-in per data-t), Caption Highlight Component, fitFontSize() Canvas Text Fitter, Per-Word Highlight Background Sweep, window.__timelines registry

### Community 10 - "Collaboration Exclusivity Scenes"
Cohesion: 0.25
Nodes (7): S5 Ensemble Scene (toi + nous), pop() Scale-In Helper, TOI + NOUS Collaboration Visual (idea sketch to product), S6 Exclu Scene (exclusivity), Exclusivity Lock + Blocked Route to Competitor, S7 Facile Scene (no problem, idea to gift), Idea Bubble to Gift Flow with Check

### Community 11 - "Long Reel npm Scripts"
Cohesion: 0.22
Nodes (8): name, private, scripts, check, dev, publish, render, type

### Community 12 - "HyperFrames Project Rules"
Cohesion: 0.29
Nodes (5): HyperFrames Composition Project (reel-court), HyperFrames skills (/hyperframes, /media-use, /hyperframes-registry), npm run check (lint after changes), HyperFrames Composition Project (reel-renardlab), npm run check (lint after changes)

### Community 13 - "DM and Share Ending"
Cohesion: 0.29
Nodes (6): DM Chat Card with Typing Indicator, S10 DM Scene (message), Send Button (870,975), End Card (logo, Metz, ECRIS-NOUS EN DM CTA), S11 Partage Scene (share + end card), Paper Plane Share to Commercant

### Community 14 - "Snow Overlay"
Cohesion: 0.47
Nodes (4): render() Flake Positioner, rnd() Deterministic Sin Hash, Snow Ambient Overlay, wholeCycles()

## Ambiguous Edges - Review These
- `Music track music.mp3 (volume 0.18)` → `"Hip-Hop Jazz" by Prospect Of Idiots (CC BY 3.0, Jamendo)`  [AMBIGUOUS]
  reel-court/index.html · relation: references

## Knowledge Gaps
- **26 isolated node(s):** `Background Music Track`, `Caption Word Pop Animation (back.out scale-in per data-t)`, `Emphasized Caption Words (.emph yellow, overshoot scale)`, `COPIE! Stamp + Shop Shake`, `Idea Bulbs (TOI vs EN FACE)` (+21 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 77 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `window.__timelines registry` connect `Word Captions System` to `Hook Products Christmas Scenes`, `Brand Printer Map Scenes`, `Collaboration Exclusivity Scenes`, `DM and Share Ending`, `Snow Overlay`, `Whip Pan Transition`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `window.__timelines registry` (e.g. with `Caption Highlight Component` and `Whip Pan Cut Transition Component`) actually correct?**
  _`window.__timelines registry` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Background Music Track`, `Caption Word Pop Animation (back.out scale-in per data-t)`, `Emphasized Caption Words (.emph yellow, overshoot scale)` to the rest of the system?**
  _26 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Reel Generators (Python)` be split into smaller, more focused modules?**
  _Cohesion score 0.09759759759759759 - nodes in this community are weakly interconnected._
- **Why does `Main Reel Composition (RenardLab3D, 50.076s portrait)` connect `Hook Products Christmas Scenes` to `Brand Printer Map Scenes`, `Word Captions System`, `Collaboration Exclusivity Scenes`, `DM and Share Ending`, `Snow Overlay`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Should `Short Reel Composition` be split into smaller, more focused modules?**
  _Cohesion score 0.13043478260869565 - nodes in this community are weakly interconnected._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Music track music.mp3 (volume 0.18)` and `"Hip-Hop Jazz" by Prospect Of Idiots (CC BY 3.0, Jamendo)`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._