from zeeman import Zeeman


def test_zeeman_mif():
    H = (0.1, -0.5, -8.9e6)
    zeeman = Zeeman(H)
    mif_string = zeeman.get_mif()
    lines = mif_string.split('\n')
    assert 'Specify Oxs_FixedZeeman {' in lines[0]
    assert '{ Oxs_UniformVectorField {' in lines[1]
    assert 'vector' in lines[2]
    line2 = lines[2].split()
    assert float(line2[1][1:]) == H[0]
    assert float(line2[2]) == H[1]
    assert float(line2[3][0:-1]) == H[2]


def test_zeeman_formatting():
    H = (0.1, -0.5, -8.9e6)
    zeeman = Zeeman(H)
    mif_string = zeeman.get_mif()
    assert mif_string[0] == 'S'
    assert mif_string[-1] == '\n'
    assert mif_string[-2] == '\n'
