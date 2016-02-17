from subprocess import Popen, PIPE, STDOUT
import os
from drivers.evolver import LLG
from drivers.evolver import Minimiser
import oommfmif as o


class Sim(object):

    def __init__(self, mesh, Ms, name=None):
        self.mesh = mesh
        self.Ms = Ms
        self.name = name
        self.gamma = 2.21e5
        self.energies = []
        self.N_Sims_Run = 0
        self._oommf_stdout = ''
        self._oommf_stderr = ''
        # Want some kind of persistent 'knowledge' of number of runs
        # and the sequence these occur in for data analysis
        # when we call a simulation multiple times to either
        # advance time or change parameters. Will need to think carefully
        # about situations such as changing H_applied - should we recreate this
        # data from the output files?
        # Advantage of this is recreating sim object if needed.

    def add(self, energy):
        self.energies.append(energy)

    def set_m(self, m_init):
        self.m_init = m_init

    def create_mif(self, evolver, overwrite=True):
        if self.name is None:
            self.name = 'unnamed'
        self.mif_filename = self.name + '_iteration' + \
            str(self.N_Sims_Run) + '.mif'
        if os.path.isfile(self.mif_filename):
            print("DEBUG: This simulation name already exists.")
            print("DEBUG: Overwriting MIF.")
        mif_file = open(self.mif_filename, 'w')
        mif_file.write('# MIF 2.1\n\n')
        mif_file.write(self.mesh.atlas_mif())
        mif_file.write(self.mesh.mesh_mif())
        for energy in self.energies:
            mif_file.write(energy.get_mif())
        mif_file.write(evolver.get_mif())
        mif_file.close()

    def run_until(self, t, alpha=0.1, gamma=2.21e5):
        llg = LLG(t, self.m_init, self.Ms, alpha, gamma, name=self.name)
        self.create_mif(llg)
        self.execute_mif()

    def minimise(self):
        minim = Minimiser(self.m_init, self.Ms, name=self.name)
        self.create_mif(minim)
        self.execute_mif()

    def execute_mif(self):
        # path = o.retrieve_oommf_path()
        # executable = o.retrieve_oommf_executable(path)
        process = o.call_oommf('boxsi ' + self.mif_filename)
        output, err = process.communicate()
        self._oommf_stdout += output
        self._oommf_stderr += err
