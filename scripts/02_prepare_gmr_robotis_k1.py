#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path("/home/ubuntu/Eunseom/motion_retarget")
GMR = ROOT / "repos/GMR"
CYCLO = ROOT / "repos/cyclo_lab"
AI_DESC = CYCLO / "third_party/ai_sapiens/ai_sapiens_description"
SRC_URDF = AI_DESC / "urdf/k1_rev1/k1.urdf"
SRC_MESH = AI_DESC / "meshes/k1_rev1"

ASSET = GMR / "assets/robotis_k1"
MESH = ASSET / "meshes"
URDF = ASSET / "k1.urdf"
IK = GMR / "general_motion_retargeting/ik_configs/smplx_to_robotis_k1.json"
PARAMS = GMR / "general_motion_retargeting/params.py"


def copy_asset() -> None:
    if not SRC_URDF.exists():
        raise FileNotFoundError(SRC_URDF)
    if not SRC_MESH.exists():
        raise FileNotFoundError(SRC_MESH)

    ASSET.mkdir(parents=True, exist_ok=True)
    if MESH.exists():
        shutil.rmtree(MESH)
    shutil.copytree(SRC_MESH, MESH)

    text = SRC_URDF.read_text()
    text = text.replace(
        'meshdir="package://ai_sapiens_description/meshes/k1_rev1"',
        'meshdir="meshes"',
    )
    text = text.replace(
        'meshdir="../../meshes/k1_rev1"',
        'meshdir="meshes"',
    )
    text = text.replace(
        "package://ai_sapiens_description/meshes/k1_rev1/",
        "",
    )
    text = text.replace(
        "../../meshes/k1_rev1/",
        "",
    )
    if 'joint name="floating_base"' not in text:
        text = text.replace(
            "  <link name=\"pelvis\">",
            "  <link name=\"world\"/>\n"
            "  <joint name=\"floating_base\" type=\"floating\">\n"
            "    <origin rpy=\"0 0 0\" xyz=\"0 0 0\"/>\n"
            "    <parent link=\"world\"/>\n"
            "    <child link=\"pelvis\"/>\n"
            "  </joint>\n"
            "  <link name=\"pelvis\">",
            1,
        )
    URDF.write_text(text)
    print(f"[ok] wrote {URDF}")


def write_ik_config() -> None:
    cfg = {
        "robot_root_name": "pelvis",
        "human_root_name": "pelvis",
        "ground_height": 0.0,
        "human_height_assumption": 1.8,
        "use_ik_match_table1": True,
        "use_ik_match_table2": True,
        "human_scale_table": {
            "head": 0.6,
            "pelvis": 0.6,
            "left_hip": 0.6,
            "right_hip": 0.6,
            "left_knee": 0.6,
            "right_knee": 0.6,
            "left_foot": 0.6,
            "right_foot": 0.6,
            "left_shoulder": 0.6,
            "right_shoulder": 0.6,
            "left_elbow": 0.6,
            "right_elbow": 0.6,
        },
        "ik_match_table1": {},
        "ik_match_table2": {},
    }
    rot = [-0.5, 0.5, 0.5, 0.5]
    # Keep this table aligned with the human body names used by the IK match
    # tables. K1 has no head link, so head is intentionally left out.
    cfg["human_scale_table"] = {
        "pelvis": 0.6,
        "left_hip": 0.6,
        "right_hip": 0.6,
        "left_knee": 0.6,
        "right_knee": 0.6,
        "left_foot": 0.6,
        "right_foot": 0.6,
        "left_shoulder": 0.6,
        "right_shoulder": 0.6,
        "left_elbow": 0.6,
        "right_elbow": 0.6,
        "left_wrist": 0.6,
        "right_wrist": 0.6,
    }
    rot_default = [-0.5, 0.5, 0.5, 0.5]
    rot_left_shoulder = [0.70710678, 0.0, -0.70710678, 0.0]
    rot_left_arm = [1.0, 0.0, 0.0, 0.0]
    rot_right_shoulder = [0.0, 0.70710678, 0.0, 0.70710678]
    rot_right_arm = [0.0, 0.0, 0.0, -1.0]
    entries = {
        "right_knee_link": ["right_knee", 0, 10, [0, 0, 0], rot_default],
        "left_knee_link": ["left_knee", 0, 10, [0, 0, 0], rot_default],
        "left_hip_yaw_link": ["left_hip", 0, 10, [0, 0, 0], rot_default],
        "right_hip_yaw_link": ["right_hip", 0, 10, [0, 0, 0], rot_default],
        "pelvis": ["pelvis", 0, 10, [0, 0, 0], rot_default],
        "left_elbow_link": ["left_elbow", 0, 10, [0, 0, 0], rot_left_arm],
        "right_elbow_link": ["right_elbow", 0, 10, [0, 0, 0], rot_right_arm],
        "left_wrist_roll_rubber_hand": ["left_wrist", 0, 10, [0, 0, 0], rot_left_arm],
        "right_wrist_roll_rubber_hand": ["right_wrist", 0, 10, [0, 0, 0], rot_right_arm],
        "left_shoulder_yaw_link": ["left_shoulder", 0, 10, [0, 0, 0], rot_left_shoulder],
        "right_shoulder_yaw_link": ["right_shoulder", 0, 10, [0, 0, 0], rot_right_shoulder],
        "left_ankle_roll_link": ["left_foot", 0, 10, [0, 0, 0], rot_default],
        "right_ankle_roll_link": ["right_foot", 0, 10, [0, 0, 0], rot_default],
    }
    cfg["ik_match_table1"] = entries
    cfg["ik_match_table2"] = {
        body: [human, 10, 5, offset, quat]
        for body, (human, _pos_w, _rot_w, offset, quat) in entries.items()
    }
    IK.write_text(json.dumps(cfg, indent=4))
    print(f"[ok] wrote {IK}")


def patch_params() -> None:
    text = PARAMS.read_text()
    if '"robotis_k1"' not in text:
        text = text.replace(
            '    "booster_k1": ASSET_ROOT / "booster_k1" / "K1_serial.xml",\n',
            '    "booster_k1": ASSET_ROOT / "booster_k1" / "K1_serial.xml",\n'
            '    "robotis_k1": ASSET_ROOT / "robotis_k1" / "k1.urdf",\n',
        )
        text = text.replace(
            '        "booster_k1": IK_CONFIG_ROOT / "smplx_to_k1.json",\n',
            '        "booster_k1": IK_CONFIG_ROOT / "smplx_to_k1.json",\n'
            '        "robotis_k1": IK_CONFIG_ROOT / "smplx_to_robotis_k1.json",\n',
        )
        text = text.replace(
            '    "booster_k1": "Trunk",\n',
            '    "booster_k1": "Trunk",\n'
            '    "robotis_k1": "pelvis",\n',
        )
        text = text.replace(
            '    "booster_k1": 2.0,\n',
            '    "booster_k1": 2.0,\n'
            '    "robotis_k1": 2.0,\n',
        )
        PARAMS.write_text(text)
        print(f"[ok] patched {PARAMS}")
    else:
        print(f"[ok] robotis_k1 already registered in {PARAMS}")


if __name__ == "__main__":
    copy_asset()
    write_ik_config()
    patch_params()
