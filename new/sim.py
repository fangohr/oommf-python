import os
from atlases import BoxAtlas
from meshes import RectangularMesh
from evolvers import RungeKuttaEvolve
from drivers import TimeDriver
from field import Field


class Sim(object):
    def __init__(self, cmin, cmax, d, Ms, name=None):
        self.cmin = cmin
        self.cmax = cmax
        self.d = d
        self.Ms = Ms
        self.name = name

        self.atlas = BoxAtlas(cmin, cmax)
        self.mesh = RectangularMesh(d)

        self.energies = []

        # Set default alpha value.
        self.alpha = 1

    def add(self, energy):
        self.energies.append(energy)

    def run_until(self, stopping_time, stages=1):
        self.evolver = RungeKuttaEvolve(self.alpha)
        self.driver = TimeDriver('evolver', stopping_time, stages, 'mesh',
                                 self.Ms, self.m0, basename=self.name)
        self.execute_mif()

    def set_m(self, m0):
        if isinstance(m0, (list, tuple, str)):
            self.m0 = m0
        elif hasattr(m0, '__call__'):
            m0field = Field(self.cmin, self.cmax, self.d, dim=3, value=m0)
            m0field.normalise(norm=self.Ms)
            m0field.write_oommf_file('m0file.omf')
            self.m0 = 'm0file.omf'

    def get_mif(self):
        mif = '# MIF 2.1\n\n'
        mif += self.atlas.get_mif()
        mif += self.mesh.get_mif()
        for i in self.energies:
            mif += i.get_mif()
        mif += self.evolver.get_mif()
        mif += self.driver.get_mif()
        
        mif += 'Destination mags mmArchive\n'
        mif += 'Schedule Oxs_TimeDriver::Spin mags Stage 1'

        return mif

    def execute_mif(self):
        self.mif_filename = self.name + '.mif'
        miffile = open(self.mif_filename, 'w')
        miffile.write(self.get_mif())
        miffile.close()

        oommf_command = 'tclsh $OOMMFTCL boxsi +fg '
        oommf_command += self.mif_filename
        oommf_command += ' -exitondone 1'
        os.system(oommf_command)
