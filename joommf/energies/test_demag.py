from demag import Demag


def test_demag_mif():
    demag = Demag()
    mif_string = demag.get_mif()
    assert 'Specify Oxs_Demag {}' in mif_string


def test_demag_formatting():
    demag = Demag()
    mif_string = demag.get_mif()
    assert mif_string[0] == 'S'
    assert mif_string[-1] == '\n'
    assert mif_string[-2] == '\n'
