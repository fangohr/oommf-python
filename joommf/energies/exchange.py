from joommf.energies.baseenergy import energy
import textwrap


class Exchange(energy):

    def __init__(self, A):
        energy.__init__(self, "Exchange")
        self.A = A

    def get_mif(self):
        exchange_mif = textwrap.dedent("""\
                       Specify Oxs_UniformExchange {{
                           A {:.2e}
                       }}\n\n""").format(self.A)
        return exchange_mif

