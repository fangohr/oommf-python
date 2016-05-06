def test_vortex():
    import joommf
    from joommf.energies import Exchange
    from joommf.energies import Demag
    import joommf.fields
    lx = ly = 50e-9
    lz = 10e-9
    dx = dy = dz = 5e-9
    Ms, A, gamma, alpha = 8e5, 1e-11, 2.21e5, 0.1
    t_sim = 2e-9  # simulation time (s)
    mesh = joommf.Mesh((lx, ly, lz), (dx, dy, dz))
    sim = joommf.Sim(mesh, Ms, name='cube_example')
    sim.add_energy(Exchange(A))
    sim.add_energy(Demag())
    sim.set_evolver(joommf.LLG(t_sim, joommf.fields.Vortex(), Ms,
                               alpha, gamma, name='cube', save_freq=1e-9))
    sim.add_output('Magnetization')
    # Run simulation.
    sim.run()
