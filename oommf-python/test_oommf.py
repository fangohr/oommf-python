def test_sim():
    import oommf as omf
    mysim = omf.sim()
    sim.settype('2d')
    sim.set_material(omf.material.Permalloy)
    sim.add_atlas(omf.atlas.BoxAtlas(x, y, z))
    sim.set_mesh('rect', [x, y, z])
    assert sim.mesh() == 'rect'
    
