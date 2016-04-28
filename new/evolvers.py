class RungeKuttaEvolve(object):
    def __init__(self, alpha, gamma_G=2.210173e5,
                 start_dm=0.01, method='rkf54'):
        if not isinstance(alpha, (int, float)) or alpha < 0:
            raise ValueError('alpha must be a positive float or int.')
        else:
            self.alpha = alpha

        if not isinstance(gamma_G, (float, int)) or gamma_G <= 0:
            raise ValueError('gamma_G must be a positive float or int.')
        else:
            self.gamma_G = gamma_G

        if not isinstance(start_dm, (float, int)) or start_dm <= 0:
            raise ValueError('start_dm must be a positive float or int.')
        else:
            self.start_dm = start_dm

        if not isinstance(method, str):
            raise ValueError('solver must be a string')
        else:
            self.method = method

    def get_mif(self):
        data = [('alpha', self.alpha),
                ('gamma_G', self.gamma_G),
                ('start_dm', self.start_dm)]

        # Create mif string.
        mif = '# RungeKutta evolver\n'
        for datum in data:
            mif += 'set {} {}\n'.format(datum[0], datum[1])
        mif += 'Specify Oxs_RungeKuttaEvolve {\n'
        mif += '\talpha $alpha\n'
        mif += '\tgamma_G $gamma_G\n'
        mif += '\tstart_dm $start_dm\n'
        mif += '\tmethod {}\n'.format(self.method)
        mif += '}\n\n'

        return mif
