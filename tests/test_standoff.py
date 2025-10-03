import pytest

from tencim1d_mesh_generator.standoff import StandoffFlexible, StandoffRigid


@pytest.mark.parametrize(
    'well_diameter,casing_external_diameter,dc,gamma,ratio',
    [
        (2.0, 1.0, 1.5, 0.0, 0.5),
        (3.0, 1.0, 1.0, 0.0, 0.0),
        (0.1, 0.01, 0.05, 0.0, 0.4444444444444444),
        (3.0, 1.0, 3.0, 0.2, 0.8),
    ],
    ids=['mesh-1', 'mesh-2', 'mesh-3', 'mesh-4'],
)
def test_standoff_rigid_ratio(well_diameter, casing_external_diameter, dc, gamma, ratio):
    standoff = StandoffRigid(casing_external_diameter, well_diameter, dc, gamma)
    assert standoff.ratio == pytest.approx(ratio)


@pytest.mark.parametrize(
    'well_diameter,casing_external_diameter,dc,sc',
    [
        (2.0, 1.0, 1.5, 0.25),
        (3.0, 1.0, 1.0, 0.0),
        (0.1, 0.01, 0.05, 0.02),
        (3.0, 1.0, 3.0, 1.0),
    ],
    ids=['mesh-1', 'mesh-2', 'mesh-3', 'mesh-4'],
)
def test_standoff_rigid_sc(well_diameter, casing_external_diameter, dc, sc):
    standoff = StandoffRigid(casing_external_diameter, well_diameter, dc)
    assert standoff.sc == pytest.approx(sc)


@pytest.mark.parametrize(
    'well_diameter,casing_external_diameter,dc,la',
    [
        (2.0, 1.0, 1.5, 0.5),
        (3.0, 1.0, 1.0, 1.0),
        (0.1, 0.01, 0.05, 0.045),
    ],
    ids=['mesh-1', 'mesh-2', 'mesh-3'],
)
def test_standoff_rigid_ls(well_diameter, casing_external_diameter, dc, la):
    standoff = StandoffRigid(casing_external_diameter, well_diameter, dc)
    assert standoff.la == pytest.approx(la)


@pytest.mark.parametrize(
    'well_diameter,casing_external_diameter,lateral_forces,restoring_force,gamma_max,ratio',
    [
        (2.0, 1.0, 1.0, 2.0, 0.1, 0.6333333333333333),
        (3.0, 1.0, 2.0, 2.0, 0.2, 0.46666666666666673),
    ],
    ids=['mesh-1', 'mesh-2'],
)
def test_standoff_flexible_ratio(
    well_diameter,
    casing_external_diameter,
    lateral_forces,
    restoring_force,
    gamma_max,
    ratio,
):
    standoff = StandoffFlexible(casing_external_diameter, well_diameter, lateral_forces, restoring_force, gamma_max)
    assert standoff.ratio == pytest.approx(ratio)
