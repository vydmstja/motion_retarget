#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import pickle
from pathlib import Path

import numpy as np

from general_motion_retargeting import GeneralMotionRetargeting as GMR
from general_motion_retargeting.utils.smpl import load_gvhmr_pred_file, get_gvhmr_data_offline_fast


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gvhmr_pred_file", required=True)
    parser.add_argument("--save_path", required=True)
    parser.add_argument("--tgt_fps", type=int, default=30)
    parser.add_argument("--robot", default="robotis_k1")
    args = parser.parse_args()

    here = Path(__file__).resolve().parents[1]
    smplx_folder = here / "assets/body_models"

    smplx_data, body_model, smplx_output, actual_human_height = load_gvhmr_pred_file(
        args.gvhmr_pred_file, smplx_folder
    )
    smplx_frames, aligned_fps = get_gvhmr_data_offline_fast(
        smplx_data, body_model, smplx_output, tgt_fps=args.tgt_fps
    )

    retarget = GMR(
        actual_human_height=actual_human_height,
        src_human="smplx",
        tgt_robot=args.robot,
        verbose=True,
        use_velocity_limit=True,
    )

    qpos_list = []
    for frame in smplx_frames:
        qpos_list.append(retarget.retarget(frame))

    qpos_arr = np.asarray(qpos_list)
    root_pos = qpos_arr[:, :3]
    root_rot_xyzw = qpos_arr[:, 3:7][:, [1, 2, 3, 0]]
    dof_pos = qpos_arr[:, 7:]

    out = {
        "fps": int(aligned_fps),
        "root_pos": root_pos,
        "root_rot": root_rot_xyzw,
        "dof_pos": dof_pos,
        "robot": args.robot,
        "robot_dof_names": retarget.robot_dof_names,
        "robot_body_names": retarget.robot_body_names,
        "robot_motor_names": retarget.robot_motor_names,
    }

    os.makedirs(os.path.dirname(args.save_path), exist_ok=True)
    with open(args.save_path, "wb") as f:
        pickle.dump(out, f)
    print(f"[ok] saved {args.save_path}")
    print(f"[ok] frames={len(qpos_list)} fps={aligned_fps} dof={dof_pos.shape[1]}")


if __name__ == "__main__":
    main()
