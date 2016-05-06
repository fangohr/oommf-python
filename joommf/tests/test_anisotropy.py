import textwrap


def test_anisotropy_axis():
    import joommf
    anisotropy = joommf.energies.UniaxialAnisotropy(530e3, [1, 0, 0])
    correct = textwrap.dedent("""\
        Specify Oxs_UniaxialAnisotropy {
        axis { 1 0 0 }
        K1 530000.0
        }
        """)
    print(correct)
    print(anisotropy.get_mif())
    assert correct == anisotropy.get_mif()


def test_anisotropy_random():
    import joommf
    anisotropy = joommf.energies.UniaxialAnisotropy(530e3, 'random')
    correct = textwrap.dedent("""\
        Specify Oxs_UniaxialAnisotropy {
        axis { Oxs_RandomVectorField {
        min_norm 1
        max_norm 1
        }
        }
        K1 530000.0
        }
        """)
    print(correct)
    print(anisotropy.get_mif())
    assert correct == anisotropy.get_mif()
