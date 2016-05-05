from joommf.energies.baseenergy import energy
import textwrap
from joommf.exceptions import JoommfError


class _Anisotropy(energy):
    pass


class UniaxialAnisotropy(_Anisotropy):

    """class UniaxialAnisotropy:
       K1, float:
           J/m^3
       axis, list or string:
           three numbers representing the axis direction
           OR 'random'
    """

    def __init__(self, K1, axis):
        energy.__init__(self, "UniaxialAnisotropy")
        self.K1 = K1
        self.axis = axis

    def get_mif(self):
        mif = textwrap.dedent("""\
        Specify Oxs_UniaxialAnisotropy {{
        axis {{ {}}}
        K1 {}
        }}
        """)
        if self.axis == 'random':
            return mif.format(textwrap.dedent("""\
                Oxs_RandomVectorField {
                min_norm 1
                max_norm 1
                }
            """), self.K1)
        else:
            vector = "{} {} {}".format(self.axis[0], self.axis[1],
                                       str(self.axis[2]) + ' ')
            return mif.format(vector, self.K1)
