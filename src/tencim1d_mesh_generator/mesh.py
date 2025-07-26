from functools import cached_property
from enum import StrEnum
from pathlib import Path

from tencim1d_mesh_generator.standoff import Standoff


type Coor = tuple[float]
type Connectivity = tuple[int, int, int]

class ThicknessEnum(StrEnum):
    THICK = 'THICK'
    THIN = 'THIN'

class Mesh:

    casing_elements_number = 20
    sheath_elements_number = 20
    formation_elements_number = 40

    formation_ratio = 1.1

    def __init__(
        self,
        internal_diameter: float,
        pipe_diameter: float,
        well_diameter: float,
        formation_diamenter: float = 60.0,
    ):
        self.internal_diameter = internal_diameter
        self.pipe_diameter = pipe_diameter
        self.well_diameter = well_diameter
        self.formation_diamenter = formation_diamenter

        self._x = []
        self._conn = []

    @cached_property
    def internal_radius(self) -> float:
        return 0.5 * self.internal_diameter

    @cached_property
    def pipe_radius(self) -> float:
        return 0.5 * self.pipe_diameter

    @cached_property
    def well_radius(self) -> float:
        return 0.5 * self.well_diameter

    @cached_property
    def formation_radius(self) -> float:
        return 0.5 * self.formation_diamenter

    @cached_property
    def casing_thickness(self) -> float:
        return self.pipe_radius - self.internal_radius

    @cached_property
    def sheath_thickness(self) -> float:
        return self.well_radius - self.pipe_radius

    @cached_property
    def formation_thickness(self) -> float:
        return self.formation_radius - self.well_radius

    @cached_property
    def element_size_casing(self) -> float:
        return self.casing_thickness / self.casing_elements_number

    @cached_property
    def element_size_sheath(self) -> float:
        return self.sheath_thickness / self.sheath_elements_number

    @cached_property
    def initial_element_size_formation(self) -> float:
        return self.formation_thickness * (self.formation_ratio - 1.0) / (self.formation_ratio ** self.formation_elements_number - 1.0)

    @cached_property
    def element_total_number(self) -> float:
        return self.casing_elements_number + self.sheath_elements_number + self.formation_elements_number

    @property
    def x(self) -> Coor:
        return self._x

    @property
    def conn(self) -> Connectivity:
        return self._conn

    @cached_property
    def effective_well_radius(self) -> float:
        return self.well_radius

    def element_size_formation(self, element_number_pos: int) -> float:
        """O tamanho do elmento segue uma PG"""
        if not 0 < element_number_pos < self.formation_elements_number:
            raise Exception('Numero de elemento invalido')
        return self.initial_element_size_formation * self.formation_ratio ** (element_number_pos - 1)

    def generate_coor(self):

        # s = 0.0
        # if thickness and self.standoff:
        #     s = self.sheath_thickness * (1.0 - self.standoff.ratio)
        #     s = s if thickness == ThicknessEnum.THICK.value else -s

        # casing
        x = [self.internal_radius]
        for node, _ in enumerate(
            range(1, self.casing_elements_number),
            start=1,
        ):
            x.append(x[node-1] + self.element_size_casing)
        x.append(self.pipe_radius)

        # Interface Steel - sheath
        x.append(self.pipe_radius)

        # Sheath
        for node, _ in enumerate(
            range(1, self.sheath_elements_number),
            start=self.casing_elements_number + 2,
        ):
            x.append(x[node-1] + self.element_size_sheath)

        # Last Node Well
        x.append(self.effective_well_radius)
        # Interface sheath - Formantion
        x.append(self.effective_well_radius)

        # Formantion
        for node, el_formation in enumerate(
            range(1, self.formation_elements_number),
            start=self.casing_elements_number + self.sheath_elements_number + 3,
        ):
            x.append(x[node-1] + self.element_size_formation(el_formation))
        x.append(self.formation_radius)

        self._x = tuple(x)

    def generate_connectivity(self):

        conn, el = [], 0

        # Casing
        for _ in range(self.casing_elements_number):
            el += 1
            conn.append((el, el+1, 1))

        # Interface Casing - Sheath
        el += 1
        conn.append((el, el+1, 2))

        # Sheath
        for _ in range(self.sheath_elements_number):
            el += 1
            conn.append((el, el+1, 3))

        # Interface Sheath - Formation
        el += 1
        conn.append((el, el+1, 2))

        # Formation
        for _ in range(self.formation_elements_number):
            el += 1
            conn.append((el, el+1, 4))

        self._conn = tuple(conn)

    def generate(self):
        self.generate_coor()
        self.generate_connectivity()

    def write(self, path: Path):

        with open(path, mode='w', encoding='utf-8') as fp:

            fp.write('coordinates\n')
            for node, x in enumerate(self.x, start=1):
                fp.write(f'{node} {x:10.4f}\n')
            fp.write('end coordinates\n')

            fp.write('bar2\n')
            for el, conn in enumerate(self.conn, start=1):
                fp.write(f'{el} {conn[0]:4} {conn[1]:4} {conn[2]:4}\n')
            fp.write('end bar2\n')

            fp.write('return\n')


class MeshWithStandoff(Mesh):

    def __init__(
        self,
        internal_diameter: float,
        pipe_diameter: float,
        well_diameter: float,
        standoff: Standoff,
        thickness: str = ThicknessEnum.THIN.value,
        formation_diamenter: float = 60.0,

    ):
        super().__init__(
            internal_diameter,
            pipe_diameter,
            well_diameter,
            formation_diamenter,
        )

        self.thickness = thickness
        self.standoff = standoff

    @cached_property
    def effective_well_radius(self) -> float:
        st = self.sheath_thickness * (1.0 - self.standoff.ratio)
        st = st if self.thickness == ThicknessEnum.THICK.value else -st

        return self.well_radius + st

    @cached_property
    def effective_sheath_thickness(self) -> float:
        return self.effective_well_radius - self.pipe_radius

    @cached_property
    def formation_thickness(self) -> float:
        return self.formation_radius - self.effective_well_radius

    @cached_property
    def element_size_sheath(self) -> float:
        return self.effective_sheath_thickness / self.sheath_elements_number


def make_mesh(
    internal_diameter: float,
    well_diameter: float,
    pipe_diameter: float,
    base_dir: Path,
    standoff: Standoff | None = None,
):

    if not base_dir.exists():
        base_dir.mkdir(exist_ok=True)

    if standoff:
        mesh = MeshWithStandoff(
            internal_diameter=internal_diameter,
            well_diameter=well_diameter,
            pipe_diameter=pipe_diameter,
            standoff=standoff,
            thickness=ThicknessEnum.THICK,
        )
        mesh.generate()
        mesh.write(path= base_dir / 'mesh_thick.dat')

        mesh = MeshWithStandoff(
            internal_diameter=internal_diameter,
            well_diameter=well_diameter,
            pipe_diameter=pipe_diameter,
            standoff=standoff,
            thickness=ThicknessEnum.THIN,
        )
        mesh.generate()
        mesh.write(path=base_dir / 'mesh_thin.dat')
    else:

        mesh = Mesh(
            internal_diameter=internal_diameter,
            well_diameter=well_diameter,
            pipe_diameter=pipe_diameter,
        )

        mesh.generate()
        mesh.write(path=base_dir / 'mesh.dat')
