class Sim(object):
    def __init__(self, mesh, Ms, name=None):
        self.mesh = mesh
        self.Ms = Ms
        self.name = name
        self.energies = []

    def add(self, energy):
        self.energies.append(energy)

    def set_m(self, m_init):
        self.m_init = m_init

    def create_mif(self):
        if self.name is None:
            self.name = 'unnamed'
        mif_filename = self.name + '.mif'
        mif_file = open(mif_filename, 'w')
        mif_file.write('# MIF 2.1\n\n')
        mif_file.write(self.mesh.atlas_mif())
        mif_file.write(self.mesh.mesh_mif())
        for energy in self.energies:
            mif_file.write(energy.get_mif())
        mif_file.close()

    def result(self):
        pass
