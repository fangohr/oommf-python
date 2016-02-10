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
                       }}""").format(self.A)
        return exchange_mif

if __name__ == '__main__':
    exchange = Exchange(1e-11)

    f = open('exchange.mif', 'w')
    f.write(exchange.get_mif())
    f.close()
