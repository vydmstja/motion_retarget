#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/home/ubuntu/Eunseom/motion_retarget}"
VIDEO="${ROOT}/videos/redred/redred_fix_44_60_white_narrow_crop.mp4"
OUT_ROOT="${ROOT}/outputs/gvhmr"
EXPECTED="${OUT_ROOT}/redred_fix_44_60_white_narrow_crop/hmr4d_results.pt"
SMPL="${ROOT}/repos/GVHMR/inputs/checkpoints/body_models/smpl/SMPL_NEUTRAL.pkl"

if [[ ! -f "${VIDEO}" ]]; then
  echo "[missing] video: ${VIDEO}"
  exit 1
fi

if [[ ! -f "${SMPL}" ]]; then
  echo "[missing] licensed SMPL file:"
  echo "          ${SMPL}"
  echo
  echo "Place SMPL_NEUTRAL.pkl there, then rerun this script."
  exit 2
fi

"${ROOT}/scripts/00_check_assets.sh"

mkdir -p "${OUT_ROOT}"
cd "${ROOT}"

docker compose -f compose.gvhmr.yaml run --rm gvhmr bash -lc '
  set -euo pipefail
  export PYTHONPATH=/workspace/GVHMR:${PYTHONPATH:-}
  python3 tools/demo/demo.py \
    --video=/workspace/videos/redred/redred_fix_44_60_white_narrow_crop.mp4 \
    --output_root=/workspace/outputs/gvhmr \
    -s
'

if [[ -f "${EXPECTED}" ]]; then
  echo "[ok] GVHMR output: ${EXPECTED}"
else
  echo "[warn] expected GVHMR output not found: ${EXPECTED}"
  find "${OUT_ROOT}" -maxdepth 3 -type f -name 'hmr4d_results.pt' -print
fi
