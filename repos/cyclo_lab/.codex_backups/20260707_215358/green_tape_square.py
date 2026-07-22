import isaaclab.sim as sim_utils
from isaaclab.assets import RigidObjectCfg


INVISIBLE_BASKET_MARKER_CFG = RigidObjectCfg(
    spawn=sim_utils.CuboidCfg(
        size=(0.01, 0.01, 0.006),
        visible=False,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            kinematic_enabled=True,
            disable_gravity=True,
        ),
        collision_props=sim_utils.CollisionPropertiesCfg(
            collision_enabled=False,
        ),
    ),
    init_state=RigidObjectCfg.InitialStateCfg(
        pos=[0.0, 0.0, 0.0],
        rot=[1.0, 0.0, 0.0, 0.0],
    ),
)

CYAN_TAPE_LONG_CFG = RigidObjectCfg(
    spawn=sim_utils.CuboidCfg(
        size=(0.24, 0.02, 0.006),
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            kinematic_enabled=True,
            disable_gravity=True,
        ),
        collision_props=sim_utils.CollisionPropertiesCfg(
            collision_enabled=False,
        ),
        visual_material=sim_utils.PreviewSurfaceCfg(
            diffuse_color=(0.0, 0.55, 0.58),
            roughness=0.75,
        ),
    ),
    init_state=RigidObjectCfg.InitialStateCfg(
        pos=[0.0, 0.0, 0.0],
        rot=[1.0, 0.0, 0.0, 0.0],
    ),
)

CYAN_TAPE_SHORT_CFG = RigidObjectCfg(
    spawn=sim_utils.CuboidCfg(
        size=(0.02, 0.24, 0.006),
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            kinematic_enabled=True,
            disable_gravity=True,
        ),
        collision_props=sim_utils.CollisionPropertiesCfg(
            collision_enabled=False,
        ),
        visual_material=sim_utils.PreviewSurfaceCfg(
            diffuse_color=(0.0, 0.55, 0.58),
            roughness=0.75,
        ),
    ),
    init_state=RigidObjectCfg.InitialStateCfg(
        pos=[0.0, 0.0, 0.0],
        rot=[1.0, 0.0, 0.0, 0.0],
    ),
)
