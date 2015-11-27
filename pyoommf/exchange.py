class Exchange(object):
    def __init__(self, A):
        self.A = A

    def exchange_mif(self):
        exchange_mif = 'Specify Oxs_UniformExchange {\n'
        exchange_mif += '\tA %2e\n' % self.A
        exchange_mif += '}\n\n'
        return exchange_mif

if __name__ == '__main__':
    exchange = Exchange(1e-11)

    f = open('exchange.mif', 'w')
    f.write(exchange.exchange_mif())
    f.close()
