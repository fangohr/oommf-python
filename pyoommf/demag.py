class Demag(object):
    def __init__(self):
        pass

    def demag_mif(self):
        demag_mif = 'Specify Oxs_Demag {}\n\n'
        return demag_mif

if __name__ == '__main__':
    demag = Demag()

    f = open('demag.mif', 'w')
    f.write(demag.demag_mif())
    f.close()
