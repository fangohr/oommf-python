class Mesh(object):
    def __init__(self, lx, ly, lz, dx, dy, dz):
        self.lx = lx
        self.ly = ly
        self.lz = lz
        self.dx = dx
        self.dy = dy
        self.dz = dz

    def mesh_info(self):
        return (self.lx, self.ly, self.lz, self.dx, self.dy, self.dz)

    def atlas_mif(self):
        atlas_mif = 'Specify Oxs_BoxAtlas:atlas {\n'
        atlas_mif += '\t xrange {0 %2e}\n' % self.lx
        atlas_mif += '\t yrange {0 %2e}\n' % self.ly
        atlas_mif += '\t zrange {0 %2e}\n' % self.lz
        atlas_mif += '}\n\n'
        return atlas_mif

mesh = Mesh(50e-9, 50e-9, 50e-9, 5-9, 5e-9, 5e-9)

f = open('mesh.mif', 'w')
f.write(mesh.atlas_mif())
f.close()
