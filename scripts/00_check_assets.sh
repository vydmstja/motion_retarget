#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/home/ubuntu/Eunseom/motion_retarget}"
GVHMR="${ROOT}/repos/GVHMR"
GMR="${ROOT}/repos/GMR"

echo "[check] workspace: ${ROOT}"
echo "[check] GVHMR: ${GVHMR}"
echo "[check] GMR: ${GMR}"

required=(
  "${GVHMR}/inputs/checkpoints/gvhmr/gvhmr_siga24_release.ckpt"
  "${GVHMR}/inputs/checkpoints/hmr2/epoch=10-step=25000.ckpt"
  "${GVHMR}/inputs/checkpoints/vitpose/vitpose-h-multi-coco.pth"
  "${GVHMR}/inputs/checkpoints/yolo/yolov8x.pt"
  "${GVHMR}/inputs/checkpoints/body_models/smplx/SMPLX_NEUTRAL.npz"
  "${GVHMR}/inputs/checkpoints/body_models/smpl/SMPL_NEUTRAL.pkl"
  "${GMR}/assets/body_models/smplx/SMPLX_NEUTRAL.pkl"
)

missing=0
for path in "${required[@]}"; do
  if [[ -f "${path}" ]]; then
    echo "[ok] ${path}"
  else
    echo "[missing] ${path}"
    missing=1
  fi
done

exit "${missing}"
