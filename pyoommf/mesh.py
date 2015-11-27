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
