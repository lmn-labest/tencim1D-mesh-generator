import pytest

from tencim1d_mesh_generator.mesh import Mesh, MeshDiameterInvalid
from tests.consts import CONNECTIVITY, COOR_CASE_1, COOR_CASE_2


@pytest.fixture
def mesh():
    return Mesh(
        1.0,
        3.0,
        6.0,
    )


def test_internal_radius(mesh: Mesh):
    assert mesh.internal_radius == pytest.approx(0.5)


def test_pipe_radius(mesh: Mesh):
    assert mesh.pipe_radius == pytest.approx(1.5)


def test_well_radius(mesh: Mesh):
    assert mesh.well_radius == pytest.approx(3.0)


def test_effective_well_radius(mesh: Mesh):
    assert mesh.effective_well_radius == pytest.approx(3.0)


def test_formation_radius(mesh: Mesh):
    assert mesh.formation_radius == pytest.approx(30.0)


def test_casing_thickness(mesh: Mesh):
    assert mesh.casing_thickness == pytest.approx(1.0)


def test_sheath_thickness(mesh: Mesh):
    assert mesh.sheath_thickness == pytest.approx(1.5)


def test_formation_thickness(mesh: Mesh):
    assert mesh.formation_thickness == pytest.approx(27.0)


def test_element_size_casing(mesh: Mesh):
    assert mesh.element_size_casing == pytest.approx(0.05)


def test_element_size_sheath(mesh: Mesh):
    assert mesh.element_size_sheath == pytest.approx(0.075)


def test_initial_element_size_formation(mesh: Mesh):
    assert mesh.initial_element_size_formation == pytest.approx(0.06100418918797616)


@pytest.mark.parametrize(
    'element_number,size',
    [
        (1, 0.06100418918797616),
        (10, 0.14384468703711567),
        (20, 0.3730960724279633),
        (30, 0.967715124752954),
    ],
    ids=[
        'element-1',
        'element-10',
        'element-20',
        'element-30',
    ],
)
def test_element_size_formation(mesh: Mesh, element_number: int, size: float):
    assert mesh.element_size_formation(element_number) == pytest.approx(size)


@pytest.mark.parametrize(
    'mesh, excepted_coors',
    [
        (Mesh(1.0, 3.0, 6.0), COOR_CASE_1),
        (Mesh(0.15716, 0.17304, 0.20955), COOR_CASE_2),
    ],
    ids=[
        'mesh-1',
        'mesh-2',
    ],
)
def test_generate_coor(mesh: Mesh, excepted_coors: list[float]):
    mesh.generate_coor()
    for node, (excepted, x) in enumerate(zip(excepted_coors, mesh.x, strict=False)):
        assert excepted == pytest.approx(x), f'Node {node + 1}'


def test_generate_connectivity(mesh: Mesh):
    mesh.generate_connectivity()

    for element, (excepted, coon) in enumerate(zip(CONNECTIVITY, mesh.conn, strict=False)):
        assert excepted == coon, f'Node {element + 1}'


def test_generate(mesh: Mesh):
    mesh.generate()

    for node, (excepted, x) in enumerate(zip(COOR_CASE_1, mesh.x, strict=False)):
        assert excepted == pytest.approx(x), f'Node {node + 1}'

    for element, (excepted_, coon) in enumerate(zip(CONNECTIVITY, mesh.conn, strict=False)):
        assert excepted_ == coon, f'Node {element + 1}'


def test_write(mesh: Mesh, tmp_path):
    mesh.generate()

    path = tmp_path / 'mesh.dat'
    mesh.write(path)

    assert path.exists()

    content = path.open().read()

    assert 'coordinates' in content
    assert 'end coordinates' in content
    assert 'bar2' in content
    assert 'end bar2' in content
    assert 'return' in content


@pytest.mark.parametrize(
    'casing_internal_diameter, casing_external_diameter, well_diameter',
    [
        (1.0, 6.0, 3.0),
        (3.0, 1.0, 6.0),
        (6.0, 3.0, 1.0),
        (6.0, 3.0, 100.0),
        (6.0, 80.0, 100.0),
        (70.0, 80.0, 100.0),
    ],
    ids=[
        'r2>r3',
        'r1>r3',
        'r1>r2>r3',
        'r3>formation',
        'r2>formation',
        'r1>formation',
    ],
)
def test_invalid_diameter(casing_internal_diameter, casing_external_diameter, well_diameter):
    with pytest.raises(MeshDiameterInvalid):
        Mesh(
            casing_internal_diameter,
            casing_external_diameter,
            well_diameter,
        )
