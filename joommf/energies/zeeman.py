from joommf.energies.baseenergy import energy


class Zeeman(energy):

    def __init__(self, H):
        energy.__init__(self, "Zeeman")
        self.H = H

    def get_mif(self):
        zeeman_mif = 'Specify Oxs_FixedZeeman {\n'
        zeeman_mif += '\tfield { Oxs_UniformVectorField {\n'
        zeeman_mif += '\t\tvector {%.5f %.5f %.5f}\n' % (self.H[0],
                                                         self.H[1],
                                                         self.H[2])
        zeeman_mif += '\t} }\n'
        zeeman_mif += '\tmultiplier 1\n'
        zeeman_mif += '}\n\n'
        return zeeman_mif

