import joommf
from joommf.energies import Exchange
from joommf.energies import Demag
from joommf.energies import FixedZeeman, UniformZeeman
lx = ly = lz = 50e-9
dx = dy = dz = 5e-9
Ms, A = 8e5, 1.3e-11
mT_conv = 795.77472
H = 200*mT_conv
m_init = (0, 0, 0)  # initial magnetisation
mesh = joommf.Mesh((lx, ly, lz), (dx, dy, dz))
sim = joommf.Sim(mesh, Ms, name='cube_example')
sim.add_energy(Exchange(A))
sim.add_energy(UniformZeeman([0, 0, 0], [0, 0, H], 30))
sim.add_energy(Demag())
sim.set_evolver(joommf.Minimiser(m_init, Ms, name='cube'))
sim.add_output('Magnetization')
# Run simulation.
sim.minimise()
sim2 = joommf.Sim(mesh, Ms, name='cube_example')
sim2.add_energy(Exchange(A))
sim2.add_energy(UniformZeeman([0, 0, 0], [0, 0, -H], 30))
sim2.add_energy(Demag())
sim2.set_evolver(joommf.Minimiser(m_init, Ms, name='cube'))
sim2.add_output('Magnetization')
# Run simulation.
sim2.minimise()

plt.plot(sim.df.UZeeman_Bz.values, sim.df.MinDriver_mz)
plt.plot(sim2.df.UZeeman_Bz.values, sim2.df.MinDriver_mz)
plt.ylim(-1.1, 1.1)
plt.xlabel('B (mT)')
plt.ylabel('Mz')
