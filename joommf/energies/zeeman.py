from joommf.energies.baseenergy import energy
import textwrap
from joommf.exceptions import JoommfError


class _Zeeman(energy):
    pass


class FixedZeeman(_Zeeman):

    def __init__(self, H):
        energy.__init__(self, "FixedZeeman")
        self.H = H
        if len(H) != 3:
            raise JoommfError(
                "Joommf: FixedZeeman only supports length"
                " 3 vectors at the present time")

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


class UniformZeeman(_Zeeman):

    """
    UniformZeeman Energy Class:
    This is a time dependent field, pass a vector of length 7 as the argument.
    Check oommf documentation for the Oxs_UZeeman class for more details.
    Args:
    [Hx_t0, Hy_t0, Hz_t0]
    [Hx_tfinal, Hy_tend, Hz_end]
    number_of_steps_through_field

    If number of steps is zero, does not change field. ?
    """

    def __init__(self, H_init, H_end, N_steps):
        energy.__init__(self, "UniformZeeman")
        self.H = [H_init[0], H_init[1], H_init[2],
                  H_end[0], H_end[1], H_end[2], N_steps]

    def get_mif(self):
        zeeman_mif = textwrap.dedent("""\
            Specify Oxs_UZeeman "Hrange {{ {{{} {} {} {} {} {} {}}} }}"
            """.format(self.H[0],
                       self.H[1],
                       self.H[2],
                       self.H[3],
                       self.H[4],
                       self.H[5],
                       self.H[6]))
        return zeeman_mif
