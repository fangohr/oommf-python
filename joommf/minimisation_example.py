def main():
    from sim import Sim
    from mesh import Mesh
    from energies.exchange import Exchange
    from energies.demag import Demag
    from energies.zeeman import Zeeman
    from drivers import evolver
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
    sim = Sim(mesh, Ms, name='minimisation_example', debug=True)

    # Add energies.
    sim.add_energy(Exchange(A))
    sim.add_energy(Demag())
    sim.add_energy(Zeeman(H))
    sim.set_evolver(evolver.Minimiser(m_init, Ms, 'test'))
    # Set initial magnetisation.
    # Run simulation.
    sim.minimise()
    print("Done")
if __name__ == "__main__":
    main()
