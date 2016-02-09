import textwrap


class Minimiser(object):

    def __init__(self, m_init, Ms, name, d_mxHxm=0.1):
        self.m_init = m_init
        self.Ms = Ms
        self.name = name
        self.d_mxHxm = d_mxHxm

    def get_mif(self):
        mif = textwrap.dedent("""\
        Specify Oxs_CGEvolve:evolver {{}}

        Specify Oxs_MinDriver {{
        evolver :evolve
        mesh :mesh
        Ms {}
        m0 {{ Oxs_UniformVectorField {{
        vector {{{:.5f}, {:.5f}, {:.5f}}}
        }} }}
        stopping_mxHxm {}
        basename {}
        vector_field_output_format {{text \%#.8g}}
        }}
        """)

        return mif.format(
            self.Ms,
            self.m_init[0],
            self.m_init[1],
            self.m_init[2],
            self.d_mxHxm,
            self.name
        )


class LLG(object):

    def __init__(self, t, m_init, Ms, alpha, gamma,
                 name, solver='rkf54', dm=0.01):
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
        self.dm = dm

    def get_mif(self):
        llg_mif = textwrap.dedent("""\
                   Specify Oxs_RungeKuttaEvolve:evolve {{
                       method ${}   alpha {:.5f}
                       gamma_G {:.5f}
                       start_dm {:.5f}
                   }}

                       Specify Oxs_TimeDriver [subst {{
                       evolver :evolve
                       stopping_time {:.2e}
                       stage_count 1
                       mesh :mesh
                       Ms {:.5e}
                       m0 {{ Oxs_UniformVectorField {{
                           vector {{{:.5f}, {:.5f}, {:.5f}}}
                       }} }}
                       basename {}
                   vector_field_output_format {{text \%#.8g}}
                   }}]


                   """)

        return llg_mif.format(self.solver,
                              self.alpha,
                              self.gamma,
                              self.dm,
                              self.t,
                              self.Ms,
                              self.m_init[0],
                              self.m_init[1],
                              self.m_init[2],
                              self.name
                              )

if __name__ == '__main__':
    llg = LLG(1e-9, (0, 0, 1), 1e6, 0.1, 2.21e5, 'test')
    f = open('test_llg.mif', 'w')
    f.write(llg.get_mif())
    f.close()
