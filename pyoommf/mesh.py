class Mesh(object):
    def __init__(self, lengths, mesh_spacing, scale=1e-9):
        assert len(lengths) == 3, "Lengths must contain three values"
        assert len(mesh_spacing) == 3, "mesh_spacing must contain a value for each coordinate direction"
        components = ['x', 'y', 'z']
        for vals, component in zip(lengths, components):
            assert vals > 0, 'L component {} must be a positive value'.format(component)
        
        self.lx = lengths[0]
        self.ly = lengths[1]
        self.lz = lengths[2]
        self.dx = mesh_spacing[0]
        self.dy = mesh_spacing[1]
        self.dz = mesh_spacing[2]
        self.scale = scale

    def mesh_info(self):
        return (self.lx, self.ly, self.lz, self.dx, self.dy, self.dz)

    def atlas_mif(self):
        atlas_mif = 'Specify Oxs_BoxAtlas:atlas {\n'
        atlas_mif += '\t xrange {0 %2e}\n' % self.lx
        atlas_mif += '\t yrange {0 %2e}\n' % self.ly
        atlas_mif += '\t zrange {0 %2e}\n' % self.lz
#        atlas_mif += '\t multiplier {%2e}\n' % self.scale
        atlas_mif += '}\n\n'
        return atlas_mif

    def mesh_mif(self):
        mesh_mif = 'Specify Oxs_RectangularMesh:mesh {\n'
        mesh_mif += '\tcellsize {%2e %2e %2e}\n' % (self.dx, self.dy, self.dz)
#        mesh_mif += '\tmultiplier {}\n'.format(self.scale)
        mesh_mif += '\tatlas :atlas\n'
        mesh_mif += '}\n\n'
        return mesh_mif

if __name__ == '__main__':
    mesh = Mesh(50e-9, 50e-9, 50e-9, 5-9, 5e-9, 5e-9)

    f = open('mesh.mif', 'w')
    f.write(mesh.atlas_mif())
    f.write(mesh.mesh_mif())
    f.close()
