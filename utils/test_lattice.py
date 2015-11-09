import lattice


def test_first_difference():
    assert lattice.first_difference([], [], reverse=False) == 0
    assert lattice.first_difference([], [], reverse=True) == 0
    assert lattice.first_difference([0], [9], reverse=False) == 0
    assert lattice.first_difference([0, 2, 4], [0, 2, 4], reverse=False) == 3
    assert lattice.first_difference([9], [9], reverse=False) == 1
    assert lattice.first_difference(['ant', 'dog', 'cat'],
                                    ['ant', 'dog', 'bird'], reverse=False) == 2
    assert lattice.first_difference(['ant', 'dog', 'cat'],
                                    ['ant', 'dog', 'bird'], reverse=True) == 0


def test_parse_lattice_spec():
    """The lattice specification should be a string such as "-5,10,5/0.5,2,2",
    which defines a two dimensional lattice where the x coordinate goes
    from -5 to 10 in 5 steps, while the y coordinate goes from 0.5 to 2 in 2
    steps. Another example is "-5,10,5/1.23,1.23,1", which defines a one
    dimensional lattice (since the y component is fixed to 1.23).
    The same can be expressed also as "-5,10,5/1.23".
    """
    s = lattice.parse_lattice_spec

    # 1d tests:
    retval = s("0,10,11")

    # data types
    assert retval == [[0., 10., 11]]
    assert isinstance(retval[0][0], float)
    assert isinstance(retval[0][1], float)
    assert isinstance(retval[0][2], int)

    # 1d data with constant
    assert s("3") == [[3, 3, 1]]

    # from docstring
    assert s("-5,10,5/1.23,1.23,1") == s("-5,10,5/1.23")

    # 2d tests
    assert s("0,3,2/-3,3,7") == [[0., 3, 2], [-3, 3, 7]]

    # from docstring
    assert s("-5,10,5/0.5,2,2") == [[-5, 10, 5], [0.5, 2, 2]]

    # 3d tests
    assert s("0,3,2/-3,3,7/-0.5,0.7,17") == [[0., 3, 2],
                                             [-3, 3, 7],
                                             [-0.5, 0.7, 17]]

    # spaces
    assert s("0,   10,   11") == [[0., 10., 11]]
