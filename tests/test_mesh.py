import pytest
from tencim1d_mesh_generator.mesh import Mesh

from tests.consts import COOR_CASE_1, COOR_CASE_2


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


def test_formation_radius(mesh: Mesh):
    assert mesh.formation_radius == pytest.approx(30.0)

def test_casing_thickness(mesh: Mesh):
    assert mesh.casing_thickness == pytest.approx(1.0)

def test_sheath_thickness(mesh: Mesh):
    assert mesh.sheath_thickness == pytest.approx(1.5)

def test_formation_thickness(mesh: Mesh):
    assert mesh.formation_thickness == pytest.approx(28.5)

def test_element_size_casing(mesh: Mesh):
    assert mesh.element_size_casing == pytest.approx(0.05)

def test_element_size_sheath(mesh: Mesh):
    assert mesh.element_size_sheath == pytest.approx(0.075)

def test_initial_element_size_formation(mesh: Mesh):
    assert mesh.initial_element_size_formation == pytest.approx(0.0643933108095304)

@pytest.mark.parametrize(
    "element_number,size",
    [
        (1, 0.0643933108095304),
        (10, 0.15183605853917767),
        (20, 0.3938236320072946),
        (30, 1.021477076128118),
    ],
    ids=[
        'element-1',
        'element-10',
        'element-20',
        'element-30',
    ]
)
def test_element_size_formation(mesh: Mesh, element_number: int, size: float):
    assert mesh.element_size_formation(element_number) == pytest.approx(size)


@pytest.mark.parametrize(
    'mesh, excepted_coors',
    [
        ( Mesh(1.0, 3.0, 6.0), COOR_CASE_1 ),
        ( Mesh(0.15716, 0.17304, 0.20955), COOR_CASE_2 ),
    ],
    ids=[
        "mesh-1",
        "mesh-2",
    ]
)
def test_generate_coor(mesh: Mesh, excepted_coors: list[float]):
    mesh.generate_coor()
    for node, (excepted, x) in enumerate(zip(excepted_coors, mesh.x)):
        assert excepted == pytest.approx(x), f'Node {node + 1}'
