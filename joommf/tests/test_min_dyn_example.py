def test_min_dyn():
    import glob
    from joommf.sim import Sim
    from joommf.mesh import Mesh
    from joommf.energies.exchange import Exchange
    from joommf.energies.demag import Demag
    from joommf.drivers import evolver
    from joommf.energies.zeeman import FixedZeeman
    # Mesh specification.
    lx = ly = lz = 50e-9  # x, y, and z dimensions (m)
    dx = dy = dz = 5e-9  # x, y, and z cell dimensions (m)

    Ms = 8e5  # saturation magnetisation (A/m)
    A = 1e-11  # exchange energy constant (J/m)
    H = (1e3, 0, 0)  # external magnetic field (A/m)
    m_init = (1, 0, 1)
    gamma = 2.21e5
    alpha = 0.1
    # Create a mesh.
    mesh = Mesh((lx, ly, lz), (dx, dy, dz))

    # Create first simulation object.
    sim1 = Sim(mesh, Ms, name='multiple_example_part1', debug=True)
    t_sim = 1e-9
    sim1.add_energy(Exchange(A))
    sim1.add_energy(Demag())
    sim1.add_energy(FixedZeeman(H))
    sim1.set_evolver(
        evolver.Minimiser(m_init, Ms, gamma))
    # Set initial magnetisation.
    # Run simulation.
    sim1.add_output('Magnetization')
    sim1.minimise()

    m_init2 = glob.glob(sim1.mif_filename[:-4] + "*.omf")[-1]
    sim2 = Sim(mesh, Ms, name='multiple_example_part2', debug=True)
    sim2.add_energy(Exchange(A))
    sim2.add_energy(Demag())
    sim2.add_energy(FixedZeeman(H))
    sim2.set_evolver(
        evolver.LLG(t_sim, m_init2, Ms, alpha, gamma, name='evolver'))
    # Set initial magnetisation.
    # Run simulation.
    sim2.run()
