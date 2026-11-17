---
name: paper-shaders
description: Animated shader backgrounds (mesh gradients, grain, halftone, liquid metal, dot orbit, waves…) from Paper Shaders (@paper-design/shaders). Use when a video, Remotion/HyperFrames composition or web page needs an animated gradient/texture background.
---

# Paper Shaders

Repo: https://github.com/paper-design/shaders · Docs and live examples: https://shaders.paper.design/

- React (Remotion): `npm i @paper-design/shaders-react` — vanilla JS/HTML (HyperFrames): `npm i @paper-design/shaders`.
- Pin an exact version: the library ships breaking changes under 0.0.x.

```jsx
import {MeshGradient} from '@paper-design/shaders-react';
<MeshGradient colors={['#5100ff','#00ff80','#ffcc00','#ea00ff']} distortion={1} swirl={0.8} speed={0.2} style={{width:'100%',height:'100%'}} />
```

For deterministic video rendering, drive the shader from the frame, not wall-clock time: set `speed={0}` and pass `frame={...}` (milliseconds) computed from the current frame (in Remotion: `useCurrentFrame() / fps * 1000`). Check the component's props in the installed package's types (`node_modules/@paper-design/shaders-react/dist/*.d.ts`) before using a shader you haven't used before.
