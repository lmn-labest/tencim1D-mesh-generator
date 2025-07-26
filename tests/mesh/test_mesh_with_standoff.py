import pytest
from tencim1d_mesh_generator.mesh import MeshWithStandoff, ThicknessEnum
from tencim1d_mesh_generator.standoff import StandoffRigid


from tests.consts import (
    COOR_CASE_3_WITH_STANDOFF_THIN,
    COOR_CASE_3_WITH_STANDOFF_THICK,
    CONNECTIVITY,
)

@pytest.fixture
def mesh_with_standoff():

    standoff = StandoffRigid(well_diameter=4.0, pipe_diameter=2.0, sc=0.8)

    return MeshWithStandoff(
        internal_diameter=1.0,
        pipe_diameter=2.0,
        well_diameter=4.0,
        standoff=standoff,
    )

@pytest.mark.parametrize(
    "thickness, expected",
    [
        (ThicknessEnum.THIN.value, 1.8),
        (ThicknessEnum.THICK.value, 2.2),
    ]
)
def test_effective_well_radius(mesh_with_standoff: MeshWithStandoff, thickness: str, expected):
    mesh_with_standoff.thickness = thickness

    assert mesh_with_standoff.effective_well_radius == pytest.approx(expected)


@pytest.mark.parametrize(
    "thickness, expected",
    [
        (ThicknessEnum.THIN.value, 0.8),
        (ThicknessEnum.THICK.value, 1.2),
    ]
)
def test_effective_sheath_thickness(mesh_with_standoff: MeshWithStandoff, thickness: str, expected):
    mesh_with_standoff.thickness = thickness

    assert mesh_with_standoff.effective_sheath_thickness == pytest.approx(expected)


@pytest.mark.parametrize(
    "thickness, expected",
    [
        (ThicknessEnum.THIN.value, 28.2),
        (ThicknessEnum.THICK.value, 27.8),
    ]
)
def test_formation_thickness(mesh_with_standoff: MeshWithStandoff, thickness: str, expected):
    mesh_with_standoff.thickness = thickness

    assert mesh_with_standoff.formation_thickness == pytest.approx(expected)


@pytest.mark.parametrize(
    "thickness, expected",
    [
        (ThicknessEnum.THIN.value, 0.04),
        (ThicknessEnum.THICK.value, 0.06),
    ]
)
def test_element_size_sheath(mesh_with_standoff: MeshWithStandoff, thickness: str, expected):
    mesh_with_standoff.thickness = thickness

    assert mesh_with_standoff.element_size_sheath == pytest.approx(expected)

@pytest.mark.parametrize(
    "thickness, expected_coor",
    [
        (ThicknessEnum.THIN.value, COOR_CASE_3_WITH_STANDOFF_THIN),
        (ThicknessEnum.THICK.value, COOR_CASE_3_WITH_STANDOFF_THICK),
    ]
)
def test_generate(
    mesh_with_standoff: MeshWithStandoff,
    thickness: str,
    expected_coor: list[float],
):

    mesh_with_standoff.thickness = thickness
    mesh_with_standoff.generate()

    for node, (excepted, x) in enumerate(zip(expected_coor, mesh_with_standoff.x)):
        assert excepted == pytest.approx(x, rel=1e-5), f'Node {node + 1}'

    for element, (excepted, coon) in enumerate(zip(CONNECTIVITY, mesh_with_standoff.conn)):
        assert excepted == coon, f'Node {element + 1}'
