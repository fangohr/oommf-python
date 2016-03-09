import joommf.mesh
import joommf.sim
from joommf.energies.demag import Demag

def test_sim_basic_square():
    testmesh = mesh.Mesh((10, 20, 30), (3, 3, 3), scale=1e-9)
    a = sim.Sim(testmesh, 1e4)
    a.add_energy(Demag())
