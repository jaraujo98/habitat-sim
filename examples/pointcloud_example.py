import pathlib

import trimesh

from habitat_sim.simulator import Simulator
from habitat_sim.utils.settings import default_sim_settings, make_cfg

EXAMPLES_DIR = pathlib.Path(__file__).parent
DATA_DIR = EXAMPLES_DIR.parent.joinpath("data")


if __name__ == "__main__":
    default_sim_settings["scene"] = DATA_DIR.joinpath(
        "versioned_data", "habitat_test_scenes", "van-gogh-room.glb"
    ).as_posix()

    cfg = make_cfg(default_sim_settings)
    sim = Simulator(cfg)

    # get the physics object attributes manager
    obj_templates_mgr = sim.get_object_template_manager()

    # get the rigid object manager
    rigid_obj_mgr = sim.get_rigid_object_manager()

    # Add an object
    # load some object templates from configuration files
    sphere_template_id = obj_templates_mgr.load_configs(
        str(DATA_DIR.joinpath("test_assets", "objects", "sphere"))
    )[0]

    # add a sphere to the scene, returns the object
    # currently a no-op since the sphere must be static for it
    # to be included in the stage mesh returned below
    sphere_obj = rigid_obj_mgr.add_object_by_template_id(sphere_template_id)

    # Get stage mesh
    verts = sim.get_stage_mesh_vertices()
    faces = sim.get_stage_mesh_face_idxs()

    mesh = trimesh.Trimesh(verts, faces)

    with open(EXAMPLES_DIR.joinpath("tmesh.glb"), "wb") as f:
        mesh.export(f, file_type="glb")

    # Sample points from stage mesh faces

    pointcloud = sim.sample_points_from_stage()
    pc = trimesh.Trimesh(pointcloud)

    with open(EXAMPLES_DIR.joinpath("tmesh_pc.obj"), "wb") as f:
        pc.export(f, file_type="obj")
