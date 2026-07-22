import isaaclab.sim as sim_utils
from isaaclab.assets import RigidObjectCfg


GREEN_TAPE_SQUARE_CFG = RigidObjectCfg(
    spawn=sim_utils.CuboidCfg(
        size=(0.24, 0.24, 0.006),
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            kinematic_enabled=True,
            disable_gravity=True,
        ),
        collision_props=sim_utils.CollisionPropertiesCfg(
            collision_enabled=False,
        ),
        visual_material=sim_utils.PreviewSurfaceCfg(
            diffuse_color=(0.0, 0.8, 0.15),
            roughness=0.7,
        ),
    ),
    init_state=RigidObjectCfg.InitialStateCfg(
        pos=[0.0, 0.0, 0.0],
        rot=[1.0, 0.0, 0.0, 0.0],
    ),
)
