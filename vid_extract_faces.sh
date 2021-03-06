#!/bin/sh
set -e

INPUT=$1
OUTDIR=`echo $INPUT | cut -d '.' -f 1 `
mkdir -p "${OUTDIR}"
OUTDIR="${OUTDIR}/"

ffmpeg -i "${INPUT}" -vf fps=1 "${OUTDIR}${INPUT}"_%03ds.png
for frame in $(dirname "${OUTDIR}${INPUT}")/*.png; do
  ./extract_faces "$frame"
done
