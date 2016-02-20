from joommf.energies.baseenergy import energy


class Demag(energy):

    def __init__(self):
        energy.__init__(self, "Demag")

    def get_mif(self):
        demag_mif = 'Specify Oxs_Demag {}\n\n'
        return demag_mif
