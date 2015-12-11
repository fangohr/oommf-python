import os
from llg import LLG

class Sim(object):
    def __init__(self, mesh, Ms, name=None):
        self.mesh = mesh
        self.Ms = Ms
        self.name = name
        self.gamma = 2.21e5
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
        mif_file.write(self.llg.get_mif())
        mif_file.write('Destination mags mmArchive\n\n')
        mif_file.write('Schedule Oxs_TimeDriver::Magnetization mags Stage 1\n\n')
        mif_file.close()

    def run_until(self, t, alpha=0.1, gamma=2.21e5):
        self.llg = LLG(t, self.m_init, self.Ms, alpha, gamma, name=self.name)
        self.create_mif()
        self.execute_mif()

    def execute_mif(self):
        command = 'tclsh $OOMMFTCL boxsi +fg ' + self.name + '.mif -exitondone 1'
        os.system(command)

