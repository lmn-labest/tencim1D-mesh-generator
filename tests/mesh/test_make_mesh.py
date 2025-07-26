from tencim1d_mesh_generator.mesh import make_mesh
from tencim1d_mesh_generator.standoff import StandoffRigid


def test_make_mesh(tmp_path):
    make_mesh(
        internal_diameter=0.15,
        well_diameter=0.17,
        pipe_diameter=0.21,
        base_dir=tmp_path / 'mesh',
    )

    assert (tmp_path / 'mesh/mesh.dat').exists()


def test_make_mesh_standoff(tmp_path):
    standoff = StandoffRigid(
        pipe_diameter=0.17,
        well_diameter=0.21,
        sc=0.01,
    )

    make_mesh(
        internal_diameter=0.15,
        pipe_diameter=0.17,
        well_diameter=0.21,
        base_dir=tmp_path / 'mesh',
        standoff=standoff,
    )

    assert (tmp_path / 'mesh/mesh_thick.dat').exists()
    assert (tmp_path / 'mesh/mesh_thin.dat').exists()
