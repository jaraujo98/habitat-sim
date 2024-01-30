import pathlib

import numpy as np

from habitat_sim.simulator import Simulator
from habitat_sim.utils.settings import default_sim_settings, make_cfg

EXAMPLES_DIR = pathlib.Path(__file__).parent
DATA_DIR = EXAMPLES_DIR.parent.joinpath("data")

if __name__ == "__main__":
    default_sim_settings["scene"] = DATA_DIR.joinpath(
        "versioned_data", "habitat_test_scenes", "apartment_1.glb"
    ).as_posix()

    cfg = make_cfg(default_sim_settings)
    sim = Simulator(cfg)

    mesh = sim.get_stage_mesh()
    stage_mesh = np.vstack(mesh)
