from functools import cached_property
from .standoff import Standoff

class StandoffInfos:
    type: str
    params: dict[str, float]


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
        standoff: Standoff | None = None,
    ):
        self.internal_diameter = internal_diameter
        self.pipe_diameter = pipe_diameter
        self.well_diameter = well_diameter
        self.formation_diamenter = formation_diamenter
        self.standoff = standoff

        self.x = []

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

    def element_size_formation(self, element_number_pos: int) -> float:
        """O tamanho do elmento segue uma PG"""
        if not 0 < element_number_pos < self.formation_elements_number:
            raise Exception('Numero de elemento invalido')
        return self.initial_element_size_formation * self.formation_ratio ** (element_number_pos - 1)

    def generate_coor(self):
        # Steel
        x = [self.internal_radius]
        for node, _ in enumerate(
            range(1, self.casing_elements_number),
            start=1,
        ):
            x.append(x[node-1] + self.element_size_casing)
        x.append(self.pipe_radius)

        # sheath
        # Interface Steel - sheath
        x.append(self.pipe_radius)
        for node, _ in enumerate(
            range(1, self.sheath_elements_number),
            start=self.casing_elements_number + 2,
        ):
            x.append(x[node-1] + self.element_size_sheath)
        x.append(self.well_radius)

        # sheath
        # Interface sheath - Formantion
        x.append(self.well_radius)
        for node, el_formation in enumerate(
            range(1, self.formation_elements_number),
            start=self.casing_elements_number + self.sheath_elements_number + 3,
        ):
            x.append(x[node-1] + self.element_size_formation(el_formation))
        x.append(self.formation_radius)

        self.x = x

    def generate(self):
        self.generate_coor()

    def write(self): ...

def make_mesh(
    internal_diameter: float,
    well_diameter: float,
    pipe_diameter: float,
    standoff: Standoff
):

    mesh = Mesh(
        internal_diameter=internal_diameter,
        well_diameter=well_diameter,
        pipe_diameter=pipe_diameter,
        standoff_ratio=standoff,
    )

    mesh.generate()
    mesh.write()
