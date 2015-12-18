from llg import LLG


def test_llg_mif():
    t = 1.5e-9
    m_init = (0, 1, 0)
    Ms = 1e6
    alpha = 0.01
    gamma = 2.21e5
    name = 'llgtest'

    llg = LLG(t, m_init, Ms, alpha, gamma, name)

    mif_string = llg.get_mif()

    lines = mif_string.split('\n')

    assert 'Specify Oxs_RungeKuttaEvolve {' in lines[0]
    line2 = lines[1].split()
    assert float(line2[1]) == alpha
    line3 = lines[2].split()
    assert float(line3[1]) == gamma
    line8 = lines[8].split()
    assert float(line8[1]) == t
    line11 = lines[11].split()
    assert float(line11[1]) == Ms
    line13 = lines[13].split()
    assert float(line13[1][1:]) == m_init[0]
    assert float(line13[2]) == m_init[1]
    assert float(line13[3][:-1]) == m_init[2]


def test_llg_formatting():
    t = 1.5e-9
    m_init = (0, 1, 0)
    Ms = 1e6
    alpha = 0.01
    gamma = 2.21e5
    name = 'llgtest'

    llg = LLG(t, m_init, Ms, alpha, gamma, name)

    mif_string = llg.get_mif()

    assert mif_string[0] == 'S'
    assert mif_string[-1] == '\n'
    assert mif_string[-2] == '\n'
