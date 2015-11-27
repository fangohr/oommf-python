import mesh
import sim

def test_sim_basic_square():
    testmesh = mesh.Mesh((10, 20, 30), (3, 3, 3), scale=1e-9)
    a = sim.Sim(testmesh, 1e4)
    
