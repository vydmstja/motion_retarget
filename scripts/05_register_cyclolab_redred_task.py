#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


ROOT = Path("/home/ubuntu/Eunseom/motion_retarget")
CYCLO = ROOT / "repos/cyclo_lab"
CFG_DIR = CYCLO / "source/cyclo_lab/cyclo_lab/simulation_tasks/manager_based/mimic/config/k1_rev1"
MOTION_NAME = "redred_44_60_white"
TASK_NAME = "RedRed4460White"


def write_env_cfg() -> None:
    target = CFG_DIR / f"{MOTION_NAME}_env_cfg.py"
    source = (CFG_DIR / "dance1_env_cfg.py").read_text()
    source = source.replace(
        "motions/K1_rev1/dance1/dance1.npz",
        f"motions/K1_rev1/{MOTION_NAME}/{MOTION_NAME}.npz",
    )
    target.write_text(source)
    print(f"[ok] wrote {target}")


def patch_init() -> None:
    init = CFG_DIR / "__init__.py"
    text = init.read_text()
    train_id = f"Cyclo-Mimic-K1-Rev1-{TASK_NAME}"
    play_id = f"Cyclo-Mimic-K1-Rev1-{TASK_NAME}-Play"
    if train_id in text:
        print("[ok] task already registered")
        return
    block = f'''

gym.register(
    id="{train_id}",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={{
        "env_cfg_entry_point": f"{{__name__}}.{MOTION_NAME}_env_cfg:K1Rev1EnvCfg",
        "rsl_rl_cfg_entry_point": f"{{agents.__name__}}.rsl_rl_ppo_cfg:K1Rev1MimicPPORunnerCfg",
    }},
)

gym.register(
    id="{play_id}",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={{
        "env_cfg_entry_point": f"{{__name__}}.{MOTION_NAME}_env_cfg:K1Rev1PlayEnvCfg",
        "rsl_rl_cfg_entry_point": f"{{agents.__name__}}.rsl_rl_ppo_cfg:K1Rev1MimicPPORunnerCfg",
    }},
)
'''
    init.write_text(text.rstrip() + block)
    print(f"[ok] registered {train_id}")
    print(f"[ok] registered {play_id}")


if __name__ == "__main__":
    write_env_cfg()
    patch_init()
