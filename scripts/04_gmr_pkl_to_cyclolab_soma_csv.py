#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import pickle

import numpy as np
from scipy.spatial.transform import Rotation as R


K1_JOINT_ORDER = [
    "left_hip_pitch_joint",
    "left_hip_roll_joint",
    "left_hip_yaw_joint",
    "left_knee_joint",
    "left_ankle_pitch_joint",
    "left_ankle_roll_joint",
    "right_hip_pitch_joint",
    "right_hip_roll_joint",
    "right_hip_yaw_joint",
    "right_knee_joint",
    "right_ankle_pitch_joint",
    "right_ankle_roll_joint",
    "waist_yaw_joint",
    "left_shoulder_pitch_joint",
    "left_shoulder_roll_joint",
    "left_shoulder_yaw_joint",
    "left_elbow_joint",
    "left_wrist_roll_joint",
    "right_shoulder_pitch_joint",
    "right_shoulder_roll_joint",
    "right_shoulder_yaw_joint",
    "right_elbow_joint",
    "right_wrist_roll_joint",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pkl", required=True)
    parser.add_argument("--out_csv", required=True)
    args = parser.parse_args()

    with open(args.pkl, "rb") as f:
        motion = pickle.load(f)

    root_pos = np.asarray(motion["root_pos"], dtype=float)
    root_quat_xyzw = np.asarray(motion["root_rot"], dtype=float)
    dof_pos = np.asarray(motion["dof_pos"], dtype=float)
    dof_names = motion.get("robot_dof_names") or {}
    name_to_idx = {name: idx for name, idx in dof_names.items() if name is not None}

    missing = [name for name in K1_JOINT_ORDER if name not in name_to_idx]
    if missing:
        raise RuntimeError(f"Missing K1 joints in GMR output: {missing}")

    # GMR records MuJoCo DoF indices, which include 6 free-joint velocity DoFs
    # before the actuated hinges. The saved dof_pos is qpos[7:], so it contains
    # only the 23 hinge qpos values.
    dof_offset = max(name_to_idx[name] for name in K1_JOINT_ORDER) + 1 - dof_pos.shape[1]
    joint_indices = [name_to_idx[name] - dof_offset for name in K1_JOINT_ORDER]
    if min(joint_indices) < 0 or max(joint_indices) >= dof_pos.shape[1]:
        raise RuntimeError(
            f"Invalid joint index mapping: offset={dof_offset}, "
            f"indices={joint_indices}, dof_pos_shape={dof_pos.shape}"
        )

    joint_pos = np.stack([dof_pos[:, idx] for idx in joint_indices], axis=1)
    root_euler = R.from_quat(root_quat_xyzw).as_euler("xyz", degrees=False)

    header = [
        "Frame",
        "root_translateX",
        "root_translateY",
        "root_translateZ",
        "root_rotateX",
        "root_rotateY",
        "root_rotateZ",
        *[f"{name}_dof" for name in K1_JOINT_ORDER],
    ]

    with open(args.out_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(root_pos.shape[0]):
            writer.writerow([i + 1, *root_pos[i], *root_euler[i], *joint_pos[i]])

    print(f"[ok] wrote {args.out_csv}")
    print(f"[ok] frames={root_pos.shape[0]} joints={joint_pos.shape[1]}")


if __name__ == "__main__":
    main()
