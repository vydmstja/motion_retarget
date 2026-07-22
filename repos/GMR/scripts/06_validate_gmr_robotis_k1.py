#!/usr/bin/env python3
import mujoco as mj

from general_motion_retargeting.params import IK_CONFIG_DICT, ROBOT_XML_DICT


robot = "robotis_k1"
print("robot_xml", ROBOT_XML_DICT[robot])
print("ik_config", IK_CONFIG_DICT["smplx"][robot])

model = mj.MjModel.from_xml_path(str(ROBOT_XML_DICT[robot]))
print("nq", model.nq, "nv", model.nv, "nu", model.nu, "nbody", model.nbody, "njnt", model.njnt)
print("joints")
for i in range(model.njnt):
    print(i, mj.mj_id2name(model, mj.mjtObj.mjOBJ_JOINT, i))
print("bodies")
for i in range(model.nbody):
    print(i, mj.mj_id2name(model, mj.mjtObj.mjOBJ_BODY, i))
