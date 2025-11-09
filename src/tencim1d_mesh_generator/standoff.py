from abc import ABC, abstractmethod

from tencim1d_mesh_generator.errors import StandoffRatioInvalid


class StandoffABC(ABC):
    @property
    @abstractmethod
    def ratio(self) -> float: ...

    def validate_ratio(self) -> bool:
        if not 0.01 <= self.ratio <= 1.0:
            raise StandoffRatioInvalid(
                f'A Razão de standoff precisa estar entre 0.01 e 1.0, valor obtido foi {self.ratio}'
            )
        return True

    def __init__(self, casing_external_diameter: float, well_diameter: float):
        self.well_diameter = well_diameter
        self.casing_external_diameter = casing_external_diameter

    @property
    def la(self) -> float:
        return (self.well_diameter - self.casing_external_diameter) * 0.5


class StandoffRigid(StandoffABC):
    def __init__(
        self,
        casing_external_diameter: float,
        well_diameter: float,
        dc: float,
        gamma_max: float = 0.0,
    ):
        super().__init__(casing_external_diameter, well_diameter)
        self.dc = dc
        self.gamma_max = gamma_max

    @property
    def sc(self) -> float:
        return 0.5 * (self.dc - self.casing_external_diameter)

    @property
    def ratio(self) -> float:
        return (self.sc - self.gamma_max) / self.la


class StandoffFlexible(StandoffABC):
    def __init__(
        self,
        casing_external_diameter: float,
        well_diameter: float,
        lateral_forces: float,
        restoring_force: float,
        gamma_max: float,
    ):
        super().__init__(casing_external_diameter, well_diameter)
        self.lateral_forces = lateral_forces
        self.restoring_force = restoring_force
        self.gamma_max = gamma_max

    @property
    def sc(self) -> float:
        return (1 - (self.lateral_forces / (3 * self.restoring_force))) * self.la

    @property
    def ratio(self) -> float:
        return (self.sc - self.gamma_max) / self.la
