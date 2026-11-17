---
name: claude-animation-base
description: Make a hand-painted 2D cartoon video (p5.js + p5.brush, Clawd character, watercolour and boiling linework) with the Claude Animation Base kit. Use when the user asks for a hand-drawn / painted cartoon or character animation video.
---

# Claude Animation Base

Kit: https://github.com/JohnHeibel/ClaudeAnimationBase

1. Get the kit (default `~/ClaudeAnimationBase`):
   `[ -d ~/ClaudeAnimationBase ] || git clone --depth 1 https://github.com/JohnHeibel/ClaudeAnimationBase ~/ClaudeAnimationBase`
   then `cd ~/ClaudeAnimationBase && npm install`. Needs Node, Chrome/Chromium and ffmpeg.
2. Read `~/ClaudeAnimationBase/ANIMATION_GUIDE.md` fully and follow its rules and workflow (storyboard first, build shot by shot, contact sheets to self-check).
3. Write the scenes in `src/scenes/`, then render:
   `node render.mjs --clip --out=out/video.mp4`
   On Linux with no GPU add `--soft-gl` (slow on watercolour fills; consider avoiding them). If Chrome isn't found pass `--chrome=/opt/pw-browsers/chromium` or set `CHROME_PATH`.
4. Copy the final MP4 to the user's project folder and tell them where it is.
