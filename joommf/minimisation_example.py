from sim import Sim
from mesh import Mesh
from energies.exchange import Exchange
from energies.demag import Demag
from energies.zeeman import Zeeman

# Mesh specification.
lx = ly = lz = 50e-9  # x, y, and z dimensions (m)
dx = dy = dz = 5e-9  # x, y, and z cell dimensions (m)

Ms = 8e5  # saturation magnetisation (A/m)
A = 1e-11  # exchange energy constant (J/m)
H = (1e3, 0, 0)  # external magnetic field (A/m)
m_init = (0, 0, 1)  # initial magnetisation

# Create a mesh.
mesh = Mesh((lx, ly, lz), (dx, dy, dz))

# Create a simulation object.
sim = Sim(mesh, Ms, name='small_example_min')

# Add energies.
sim.add(Exchange(A))
sim.add(Demag())
sim.add(Zeeman(H))


# Set initial magnetisation.
sim.set_m(m_init)

# Run simulation.
sim.minimise()
