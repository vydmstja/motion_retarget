# motion_retarget

Red Red 44-60s motion-retargeting workspace for ROBOTIS K1.

This repository contains the code, Docker files, scripts, final retargeted motion outputs, and the final Sim2Real deployment bundle used for the K1 Red Red motion experiment.

## Included

- `compose.gvhmr.yaml`
- `docker/gvhmr.Dockerfile`
- `scripts/`
- `videos/redred/`
- `outputs/gmr/redred_44_60_robotis_k1.pkl`
- `repos/GVHMR/`
- `repos/GMR/`
- `repos/cyclo_lab/`
- `repos/ai_sapiens/`
- `sim2real_bundle/`

## Sim2Real Bundle

The final deployment bundle is:

```text
sim2real_bundle/
  exported/policy.onnx
  params/sim2real.yaml
  params/redred_44_60_white.csv
  backup/model_2999.pt
  backup/redred_44_60_white.npz
```

The final training run used for export was:

```text
cyclo_mimic_k1_rev1_redred4460white/
2026-07-16_13-27-59_redred_44_60_corrected2_4096env_3000it/model_2999.pt
```

## Excluded

Large downloaded checkpoints, HDF5 datasets, Isaac Sim runtime files, and licensed SMPL/SMPL-X body model files are intentionally excluded from Git.

Examples:

- GVHMR/VitPose/YOLO checkpoints
- SMPL and SMPL-X model files
- Cyclo Lab generated datasets
- Isaac Sim runtime cache

Download these files separately according to their original project instructions and licenses.
