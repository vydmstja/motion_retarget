import isaaclab.sim as sim_utils
from isaaclab.assets import RigidObjectCfg


RED_BLOCK_CFG = RigidObjectCfg(
    spawn=sim_utils.CuboidCfg(
        size=(0.06, 0.06, 0.06),
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            linear_damping=3.0,
            angular_damping=3.0,
        ),
        collision_props=sim_utils.CollisionPropertiesCfg(),
        mass_props=sim_utils.MassPropertiesCfg(mass=0.08),
        physics_material=sim_utils.RigidBodyMaterialCfg(
            static_friction=0.8,
            dynamic_friction=0.6,
            restitution=0.0,
        ),
        visual_material=sim_utils.PreviewSurfaceCfg(
            diffuse_color=(1.0, 0.0, 0.0),
            roughness=0.5,
        ),
    ),
    init_state=RigidObjectCfg.InitialStateCfg(
        pos=[0.0, 0.0, 0.0],
        rot=[1.0, 0.0, 0.0, 0.0],
    ),
)
