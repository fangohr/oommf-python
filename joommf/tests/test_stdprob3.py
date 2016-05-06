def test_stdprob3():
    import numpy as np
    from scipy.constants import mu_0
    import joommf
    from joommf.energies import Exchange
    from joommf.energies import Demag
    from joommf.energies import UniaxialAnisotropy
    import scipy.optimize
    import joommf.fields

    N = 16
    cubesize = 100e-9
    Km = 1e6
    K1 = 0.1*Km
    Ms = np.sqrt(2 * Km/mu_0)
    cellsize = cubesize/N
    mesh = joommf.Mesh(
        (cubesize, cubesize, cubesize), (cellsize, cellsize, cellsize))

    def VortexSim(L):
        lex = cubesize/L
        A = 0.5*mu_0*Ms*Ms*lex**2
        sim = joommf.Sim(mesh, Ms, name='vort')
        sim.add_energy(Exchange(A))
        sim.add_energy(Demag())
        sim.add_energy(UniaxialAnisotropy(K1, [0, 0, 1]))
        sim.set_evolver(
            joommf.Minimiser(joommf.fields.Vortex(), Ms, name='test'))
        sim.add_output('Magnetization')
        # Run simulation.
        sim.minimise()
        return sim.df.CGEvolve_evolver_Total_energy.values[-1]*10**16

    def TwistedSim(L):
        lex = cubesize/L
        A = 0.5*mu_0*Ms*Ms*lex**2
        sim = joommf.Sim(mesh, Ms, name='twis')
        sim.add_energy(Exchange(A))
        sim.add_energy(Demag())
        sim.add_energy(UniaxialAnisotropy(K1, [0, 0, 1]))
        sim.set_evolver(
            joommf.Minimiser(joommf.fields.Twisted(), Ms, name='test'))
        sim.add_output('Magnetization')
        # Run simulation.
        sim.minimise()
        return sim.df.CGEvolve_evolver_Total_energy.values[-1]*10**16

    def Bisector(L):
        a = VortexSim(L)
        b = TwistedSim(L)
        print(L, a, b, a - b)
        return a - b

    L = scipy.optimize.bisect(Bisector, 8, 8.5, xtol=1e-3)
    np.testing.assert_almost_equal(L - 8.4677, 0, decimal=3)
