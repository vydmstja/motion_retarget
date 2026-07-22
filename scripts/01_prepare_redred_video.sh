#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/home/ubuntu/Eunseom/motion_retarget}"
URL="${URL:-https://www.youtube.com/watch?v=kuVNutQeBBA}"
START="${START:-00:00:44}"
END="${END:-00:01:00}"
OUT_DIR="${ROOT}/videos/redred"

mkdir -p "${OUT_DIR}"

if ! command -v yt-dlp >/dev/null 2>&1; then
  if [[ -x "${HOME}/.local/bin/yt-dlp" ]]; then
    YTDLP="${HOME}/.local/bin/yt-dlp"
  else
    python3 -m pip install --user -q yt-dlp
    YTDLP="${HOME}/.local/bin/yt-dlp"
  fi
else
  YTDLP="yt-dlp"
fi

SOURCE="${OUT_DIR}/redred_fix_44_60_source.mp4"
SELECTED="${OUT_DIR}/redred_fix_44_60_white_narrow_crop.mp4"

"${YTDLP}" \
  --download-sections "*${START}-${END}" \
  -f "bv*[height<=1080]+ba/b[height<=1080]" \
  --merge-output-format mp4 \
  -o "${OUT_DIR}/redred_fix_44_60_source.%(ext)s" \
  "${URL}"

/usr/bin/ffmpeg -y -i "${SOURCE}" \
  -vf "crop=550:ih:1000:0,scale=720:-2,fps=30" \
  -an "${SELECTED}"

echo "[done] source clip: ${SOURCE}"
echo "[done] selected GVHMR input: ${SELECTED}"
