def test_sim():
    import oommf as omf
    mysim = omf.sim()
    sim.settype('2d')
    sim.set_material(omf.material.Permalloy)
    sim.add_atlas(omf.atlas.BoxAtlas(x, y, z))
    sim.set_mesh('rect', [x, y, z])
    sim.dmdt(0.01)
    sim.set_uniform_magnetisation([0, 0, 1], 10e-9)
    sim.set_field([0, 0, -1], 1)
    sim.addEnergy('exchange')
    sim.addEnergy('anisotropy')
    sim.addEnergy('zeeman')
    sim.addEnergy('DMI')
