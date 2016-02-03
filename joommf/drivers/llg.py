class LLG(object):

    def __init__(self, t, m_init, Ms, alpha, gamma, name, solver='rkf54'):
        """
        Note: 
        solver options passed as a string - options
        rk2, rk4, rkf54, rkf54m, rkf54s

        """
        self.t = t
        self.m_init = m_init
        self.Ms = Ms
        self.alpha = alpha
        self.gamma = gamma
        self.name = name
        self.solver = solver

    def get_mif(self):
        llg_mif = 'Specify Oxs_RungeKuttaEvolve:evolve {\n'
        llg_mif += '\tmethod ${}'.format(self.solver)
        llg_mif += '\talpha %.5f\n' % self.alpha
        llg_mif += '\tgamma_G %.5f\n' % self.gamma
        llg_mif += '\tstart_dm 0.01\n'
        llg_mif += '}\n\n'

        llg_mif += 'Specify Oxs_TimeDriver [subst {\n'
        llg_mif += '\tevolver :evolve\n'
        llg_mif += '\tstopping_time %2e\n' % self.t
        llg_mif += '\tstage_count 1\n'
        llg_mif += '\tmesh :mesh\n'
        llg_mif += '\tMs %2e\n' % self.Ms
        llg_mif += '\tm0 { Oxs_UniformVectorField {\n'
        llg_mif += '\t\tvector {%.5f %.5f %.5f}\n' % (
            self.m_init[0], self.m_init[1], self.m_init[2])
        llg_mif += '\t} }\n'
        llg_mif += '\tbasename ' + self.name + ' \n'
        llg_mif += 'vector_field_output_format {text \%#.8g}\n'
        llg_mif += '}]\n\n'
        return llg_mif

if __name__ == '__main__':
    llg = LLG(1e-9, (0, 0, 1), 1e6, 0.1, 2.21e5, 'test')
    f = open('llg.mif', 'w')
    f.write(llg.get_mif())
    f.close()
