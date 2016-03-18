from joommf.energies.exchange import Exchange


def test_exchange_mif():
    A = 1e-11
    exchange = Exchange(A)
    mif_string = exchange.get_mif()
    lines = mif_string.split('\n')
    assert 'Specify Oxs_UniformExchange {' in lines[0]
    assert 'A' in lines[1]
    assert float(lines[1].split()[1]) == A
    assert '}' in lines[2]


def test_exchange_formatting():
    A = 1e-11
    exchange = Exchange(A)
    mif_string = exchange.get_mif()
    assert mif_string[0] == 'S'
