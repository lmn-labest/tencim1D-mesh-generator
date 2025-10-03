import pytest

from tencim1d_mesh_generator.mesh import make_mesh
from tencim1d_mesh_generator.standoff import StandoffRatioInvalid, StandoffRigid


def test_make_mesh(tmp_path):
    make_mesh(
        casing_internal_diameter=0.15,
        casing_external_diameter=0.17,
        well_diameter=0.21,
        base_dir=tmp_path / 'mesh',
    )

    assert (tmp_path / 'mesh/mesh.dat').exists()


def test_make_mesh_standoff(tmp_path):
    standoff = StandoffRigid(
        casing_external_diameter=0.17,
        well_diameter=0.21,
        dc=0.19,
    )

    make_mesh(
        casing_internal_diameter=0.15,
        casing_external_diameter=0.17,
        well_diameter=0.21,
        base_dir=tmp_path / 'mesh',
        standoff=standoff,
    )

    assert (tmp_path / 'mesh/mesh_thick.dat').exists()
    assert (tmp_path / 'mesh/mesh_thin.dat').exists()


def test_make_mesh_standoff_invalid_ratio(tmp_path):
    standoff = StandoffRigid(
        casing_external_diameter=0.17,
        well_diameter=0.21,
        dc=0.17,
    )

    with pytest.raises(StandoffRatioInvalid):
        make_mesh(
            casing_internal_diameter=0.15,
            casing_external_diameter=0.17,
            well_diameter=0.21,
            base_dir=tmp_path / 'mesh',
            standoff=standoff,
        )

    assert not (tmp_path / 'mesh/mesh_thick.dat').exists()
    assert not (tmp_path / 'mesh/mesh_thin.dat').exists()
