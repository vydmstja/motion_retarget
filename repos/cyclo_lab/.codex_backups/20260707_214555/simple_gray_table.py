import isaaclab.sim as sim_utils
from isaaclab.assets import RigidObjectCfg


SIMPLE_GRAY_TABLE_CFG = RigidObjectCfg(
    spawn=sim_utils.CuboidCfg(
        size=(0.90, 0.65, 0.08),
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            kinematic_enabled=True,
            disable_gravity=True,
        ),
        collision_props=sim_utils.CollisionPropertiesCfg(),
        visual_material=sim_utils.PreviewSurfaceCfg(
            diffuse_color=(0.12, 0.12, 0.12),
            roughness=0.55,
        ),
    ),
    init_state=RigidObjectCfg.InitialStateCfg(
        pos=[0.0, 0.0, 0.68],
        rot=[1.0, 0.0, 0.0, 0.0],
    ),
)
