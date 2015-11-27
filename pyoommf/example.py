import sim, mesh

# Mesh specification.
lx = ly = lz = 50e-9  # x, y, and z dimensions (m)
dx = dy = dz = 5e-9  # x, y, and z cell dimensions (m)

Ms = 8e5  # saturation magnetisation (A/m)
A = 1e-11  # exchange energy constant (J/m)
H = (1e6, 0, 0)  # external magnetic field (A/m)
m_init = (0, 0, 1)  # initial magnetisation
t_sim = 1e-9  # simulation time (s)

# Create a mesh.
mesh = mesh.Mesh(lx, ly, lz, dx, dy, dz)

# Create a simulation object.
sim = sim.Sim(mesh, Ms)

# Add energies.
sim.add_exchange(A)
sim.add_demag()
sim.add_zeeman(H)

# Set initial magnetisation.
sim.set_m(m_init)

# Run simulation.
sim.run_until(t_sim)

# Get the results.
results = sim.result()
