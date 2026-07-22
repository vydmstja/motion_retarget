#!/usr/bin/env bash
set -euo pipefail

ROOT="${ROOT:-/home/ubuntu/Eunseom/motion_retarget}"
PKL="${ROOT}/outputs/gmr/redred_44_60_robotis_k1.pkl"
MOTION_DIR="${ROOT}/repos/cyclo_lab/source/cyclo_lab/data/motions/K1_rev1/redred_44_60_white"
CSV="${MOTION_DIR}/redred_44_60_white_soma.csv"
NPZ="${MOTION_DIR}/redred_44_60_white.npz"

if [[ ! -f "${PKL}" ]]; then
  echo "[missing] GMR result: ${PKL}"
  echo "Run scripts/09_run_gmr_robotis_k1.sh first."
  exit 1
fi

mkdir -p "${MOTION_DIR}"

docker run --rm \
  -v "${ROOT}/repos/GMR:/workspace/GMR" \
  -v "${ROOT}/outputs:/workspace/outputs" \
  -v "${MOTION_DIR}:/workspace/redred_motion" \
  -w /workspace/GMR \
  humanoids2026-gmr:py310 \
  python scripts/04_gmr_pkl_to_cyclolab_soma_csv.py \
    --pkl /workspace/outputs/gmr/redred_44_60_robotis_k1.pkl \
    --out_csv /workspace/redred_motion/redred_44_60_white_soma.csv

docker exec cyclo_lab bash -lc '
  set -euo pipefail
  cd /workspace/cyclo_lab
  ./third_party/IsaacLab/isaaclab.sh -p scripts/tools/motion/soma_retargeter_csv_converter.py \
    -f source/cyclo_lab/data/motions/K1_rev1/redred_44_60_white/redred_44_60_white_soma.csv \
    --output_name source/cyclo_lab/data/motions/K1_rev1/redred_44_60_white/redred_44_60_white.npz \
    --position-scale 1 \
    --angle-unit radians \
    --root-height-offset 0.22 \
    --smooth-window 3 \
    --smooth-passes 1 \
    --smooth-fields root_pos root_rot joints \
    --headless
'

echo "[ok] Cyclo Lab CSV: ${CSV}"
echo "[ok] Cyclo Lab NPZ: ${NPZ}"
