import mesh
import sim
from energies.demag import Demag

def test_sim_basic_square():
    testmesh = mesh.Mesh((10, 20, 30), (3, 3, 3), scale=1e-9)
    sim.Sim(testmesh, 1e4)
    sim.add_energy(Demag())
