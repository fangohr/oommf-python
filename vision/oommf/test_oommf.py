def test_oommf_sim():
    import oommf
    import os.path
    oommf.path = "/home/vagrant/oommf-python/oommf/oommf/"
    Py = oommf.materials.permalloy
    my_geometry = oommf.geometry.Cuboid(
        (0, 0, 0), (30, 30, 100), unitlength=1e-9)
    sim = oommf.Simulation(my_geometry, cellsize=5e-9, material=Py)
    sim.m = [1, 1, 0]
    assert str(sim) == 'Simulation: Py(Fe80Ni20). \n\t'  \
                       + 'Geometry: Cuboid corner1 = (0, 0, 0), ' \
                       + 'corner2 = (30, 30, 100). \n\t      ' \
                       + '    Cells = [6, 6, 20], total=720.'
    sim.advance_time(1e-9)
    assert str(sim) == 'Simulation: Py(Fe80Ni20). \n\tGeometry: ' \
        + 'Cuboid corner1 = (0, 0, 0), '\
        + ' corner2 = (30, 30, 100). \n\t  ' \
                       + \
        '        Cells = [6, 6, 20], total=720.\n\tCurrent t = 1e-09s'

    assert os.path.isfile('Simulation_0.0_1e-09.mif')
    os.system('rm Simulation_0.0_1e-09.mif')


def test_mif_assemble():
    import oommf
    import oommf.mifgen
    NiFe = oommf.materials.NiFe
    my_geometry = oommf.geometry.Cuboid(
        (0, 0, 0), (310, 310, 40), unitlength=1e-9)
    sim = oommf.Simulation(my_geometry, cellsize=5e-9, material=NiFe)
    mifpath = oommf.mifgen._assemble_mif(sim)
    f = open(mifpath, 'r')
    f2 = open('oommf.oommfpath' + '/app/oxs/examples/square.mif')
    constructed_miffile = f.read()
    read_miffile = f2.read()
    assert constructed_miffile == read_miffile


def test_material():
    import oommf.materials
    assert str(oommf.materials.Permalloy) == 'Py(Fe80Ni20)'
    assert oommf.materials.Permalloy.A == 13e-12
