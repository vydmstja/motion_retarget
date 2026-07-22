#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/home/ubuntu/Eunseom/motion_retarget}"
PRED="${ROOT}/outputs/gvhmr/redred_fix_44_60_white_narrow_crop/hmr4d_results.pt"
OUT="${ROOT}/outputs/gmr/redred_44_60_robotis_k1.pkl"

if [[ ! -f "${PRED}" ]]; then
  echo "[missing] GVHMR result: ${PRED}"
  echo "Run scripts/08_run_gvhmr_redred.sh first."
  exit 1
fi

mkdir -p "$(dirname "${OUT}")"

docker run --rm --gpus all \
  -v "${ROOT}/repos/GMR:/workspace/GMR" \
  -v "${ROOT}/outputs:/workspace/outputs" \
  -w /workspace/GMR \
  humanoids2026-gmr:py310 \
  python scripts/03_gvhmr_to_robotis_k1_headless.py \
    --gvhmr_pred_file /workspace/outputs/gvhmr/redred_fix_44_60_white_narrow_crop/hmr4d_results.pt \
    --save_path /workspace/outputs/gmr/redred_44_60_robotis_k1.pkl

echo "[ok] GMR output: ${OUT}"
