from abc import ABC, abstractmethod


class Standoff(ABC):
    def __init__(self, casing_external_diameter: float, well_diameter: float):
        self.well_diameter = well_diameter
        self.casing_external_diameter = casing_external_diameter

    @property
    @abstractmethod
    def ratio(self) -> float: ...

    @property
    def la(self) -> float:
        return (self.well_diameter - self.casing_external_diameter) * 0.5


class StandoffRigid(Standoff):
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


class StandoffFlexible(Standoff):
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
