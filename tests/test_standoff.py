import pytest

from tencim1d_mesh_generator.standoff import StandoffFlexible, StandoffRigid


@pytest.mark.parametrize(
    'well_diameter,casing_external_diameter,sc,ratio',
    [
        (2.0, 1.0, 0.4, 0.8),
        (3.0, 1.0, 0.4, 0.4),
        (0.1, 0.01, 0.01, 0.2222222222222222),
    ],
    ids=['mesh-1', 'mesh-2', 'mesh-3'],
)
def test_standoff_rigid_ratio(well_diameter, casing_external_diameter, sc, ratio):
    standoff = StandoffRigid(casing_external_diameter, well_diameter, sc)
    assert standoff.ratio == pytest.approx(ratio)


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
