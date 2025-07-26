from src.tencim1d_mesh_generator.mesh import make_mesh
from src.tencim1d_mesh_generator.standoff import StandoffRigid


internal_diameter=1.0
pipe_diameter=2.0
well_diameter=4.0
sc = 0.8

standoff = StandoffRigid(
    well_diameter=well_diameter,
    pipe_diameter=pipe_diameter,
    sc=sc,
)

make_mesh(
    internal_diameter=internal_diameter,
    pipe_diameter=pipe_diameter,
    well_diameter=well_diameter,
    standoff=standoff,
)
