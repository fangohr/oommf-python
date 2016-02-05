from baseenergy import energy


class Exchange(energy):

    def __init__(self, A):
        energy.__init__(self, "Exchange")
        self.A = A

    def get_mif(self):
        exchange_mif = 'Specify Oxs_UniformExchange {\n'
        exchange_mif += '\tA %2e\n' % self.A
        exchange_mif += '}\n\n'
        return exchange_mif

if __name__ == '__main__':
    exchange = Exchange(1e-11)

    f = open('exchange.mif', 'w')
    f.write(exchange.get_mif())
    f.close()
