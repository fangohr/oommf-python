def test_oommf_sim():
    import oommf
    import os.path
    oommf.path = "/home/vagrant/oommf-python/oommf/oommf/"
    Py = oommf.materials.permalloy
    my_geometry = oommf.geometry.Cuboid((0,0,0), (30, 30, 100), unitlength=1e-9)
    sim = oommf.Simulation(my_geometry, cellsize=5e-9, material=Py)
    sim.m = [1, 1, 0]
    assert str(sim) == 'Simulation: Py(Fe80Ni20). \n\tGeometry: Cuboid corner1 = (0, 0, 0), corner2 = (30, 30, 100). \n\t  ' \
                       + '        Cells = [6, 6, 20], total=720.'
    sim.advance_time(1e-9)
    assert str(sim) == 'Simulation: Py(Fe80Ni20). \n\tGeometry: Cuboid corner1 = (0, 0, 0), corner2 = (30, 30, 100). \n\t  ' \
                       + '        Cells = [6, 6, 20], total=720.\n\tCurrent t = 1e-09s'

    assert os.path.isfile('Simulation_0.0_1e-09.mif')
    os.system('rm Simulation_0.0_1e-09.mif')



