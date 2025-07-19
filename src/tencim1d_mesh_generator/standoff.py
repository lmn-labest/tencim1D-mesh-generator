from abc import ABC, abstractmethod


class Standoff(ABC):
    def __init__(self, well_diameter: float, pipe_diameter: float):
        self.well_diameter = well_diameter
        self.pipe_diameter = pipe_diameter

    @property
    @abstractmethod
    def ratio(self) -> float: ...

class StandoffRigid(Standoff):
    def __init__(self, well_diameter: float, pipe_diameter: float, sc: float):
        super().__init__(well_diameter, pipe_diameter)
        self.sc = sc

    @property
    def ratio(self) -> float:
        return 2.0 * self.sc / (self.well_diameter - self.pipe_diameter)

class StandoffFlexible(Standoff):
    def __init__(
        self,
        well_diameter: float,
        pipe_diameter: float,
        lateral_forces: float,
        restoring_force: float,
        gamma_max: float,
    ):
        super().__init__(well_diameter, pipe_diameter)
        self.lateral_forces = lateral_forces
        self.restoring_force = restoring_force
        self.gamma_max = gamma_max

    @property
    def ratio(self) -> float:
        la = (self.well_diameter - self.pipe_diameter) * 0.5
        sc = (1 - (self.lateral_forces / (3 * self.restoring_force) )) * la
        return (sc - self.gamma_max) / la
