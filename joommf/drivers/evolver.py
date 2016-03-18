import textwrap
from joommf.exceptions import JoommfError
import os


class Evolver(object):

    def __init__(self):
        pass


class Minimiser(Evolver):

    def __init__(self, m_init, Ms, d_mxHxm=0.1):
        if isinstance(m_init, str):
            if os.isfile(m_init):
                self.m_init = m_init
            else:
                raise JoommfError("Magnetisation file not found")
        else:
            self.m_init = m_init
        # Want to throw a warning here if neither
        self.Ms = Ms
        self.d_mxHxm = d_mxHxm
        self.name = None

    def _setname(self, name):
        self.name = name

    def get_mif(self):
        if isinstance(self.m_init, str):
            self.m0 = textwrap.dedent("""\
                m0 {{ Oxs_FileVectorField {{
                file {}
                atlas :atlas
                }} }}
                """)

        else:
            self.m0 = textwrap.dedent("""\
                m0 {{ Oxs_UniformVectorField {{
                norm 1
                vector {{{} {} {}}}
                }} }}
                """.format(self.m_init[0],
                           self.m_init[1],
                           self.m_init[2]))

        mif = textwrap.dedent("""\
        Specify Oxs_CGEvolve:evolver {{}}

        Specify Oxs_MinDriver [subst {{
        evolver :evolver
        mesh :mesh
        Ms {}
        {}

        stopping_mxHxm {}
        basename {}
        vector_field_output_format {{text \%#.8g}}
        }}]
        """)

        return mif.format(
            self.Ms,
            self.m0,
            self.d_mxHxm,
            self.name
        )


class LLG(Evolver):

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
        self.name = None
        self.solver = solver
        self.dm = dm

    def _setname(self, name):
        self.name = name

    def get_mif(self):
        if isinstance(self.m_init, str):
            self.m0 = textwrap.dedent("""\
                m0 {{ Oxs_FileVectorField {{
                file {}
                atlas :atlas
                }} }}
                """.format(self.m_init))
        else:
            self.m0 = textwrap.dedent("""\
                m0 {{ Oxs_UniformVectorField {{
                norm 1
                vector {{{} {} {}}}
                }} }}
                """.format(self.m_init[0],
                           self.m_init[1],
                           self.m_init[2]))

        llg_mif = textwrap.dedent("""\
                   Specify Oxs_RungeKuttaEvolve:evolve {{
                       method {}   alpha {:.5f}
                       gamma_G {:.5f}
                       start_dm {:.5f}
                   }}

                       Specify Oxs_TimeDriver [subst {{
                       evolver :evolve
                       stopping_time {:.2e}
                       stage_count 1
                       mesh :mesh
                       Ms {}
                       {}
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
                              self.m0,
                              self.name
                              )

if __name__ == '__main__':
    llg = LLG(1e-9, (0, 0, 1), 1e6, 0.1, 2.21e5, 'test')
    f = open('test_llg.mif', 'w')
    f.write(llg.get_mif())
    f.close()
