from baseenergy import energy


class Demag(energy):

    def __init__(self):
        energy.__init__(self, "Demag")

    def get_mif(self):
        demag_mif = 'Specify Oxs_Demag {}\n\n'
        return demag_mif

if __name__ == '__main__':

    demag = Demag()
    f = open('demag.mif', 'w')
    f.write(demag.get_mif())
    f.close()
