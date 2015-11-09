import lattice


def test_first_difference():
    assert lattice.first_difference([0], [9], reverse=False) == 0
    # the following two fail


def test_first_difference_regression1():
    assert lattice.first_difference([0, 2, 4], [0, 2, 4], reverse=False) == 3


def test_first_difference_regression2():
    assert lattice.first_difference([9], [9], reverse=False) == 1
