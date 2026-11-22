#!/bin/sh
# Codifica la secuencia de anim_camara.py y la deja en assets/camara/ (uso: montar_camara.sh <carpeta con A_*.png, B_*.png, bgA.png>)
set -e
SEQ="$1"; DST="$(dirname "$0")/../assets/camara"; mkdir -p "$DST"
cp "$SEQ/bgA.png" "$DST/bgA.png"
ffmpeg -y -loglevel error -framerate 30 -i "$SEQ/A_%04d.png" -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 20 -auto-alt-ref 0 "$DST/giroA.webm"
ffmpeg -y -loglevel error -framerate 30 -start_number 57 -i "$SEQ/B_%04d.png" -c:v libx264 -pix_fmt yuv420p -crf 14 -preset slow "$DST/B.mp4"
LAST=$(ls "$SEQ"/B_*.png | tail -1); cp "$LAST" "$DST/final.png"
echo "montado: $DST"
