class Zeeman(object):
    def __init__(self, H):
        self.H = H

    def get_mif(self):
        zeeman_mif = 'Specify Oxs_FixedZeeman {\n'
        zeeman_mif += '\tfield { Oxs_UniformVectorField {\n'
        zeeman_mif += '\t\tvector {%.5f %.5f %.5f}\n' % (self.H[0], self.H[1], self.H[2])
        zeeman_mif += '\t} }\n'
        zeeman_mif += '\tmultiplier 1\n'
        zeeman_mif += '}\n\n'
        return zeeman_mif

if __name__ == '__main__':
    exchange = Zeeman((0, 0, 1))

    f = open('zeeman.mif', 'w')
    f.write(exchange.get_mif())
    f.close()
