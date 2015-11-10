import numpy as np
import pytest

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


def test_lattice_object_1d():
    l = lattice.Lattice([[0, 10, 6]])
    assert l.dim == 1

    check_points_index = []
    check_points_value = []

    def f(idx, x):
        print("idx = {} x={}".format(idx, x))
        check_points_index.append(idx[0])
        check_points_value.append(x[0])

    l.foreach(f)

    assert check_points_index == list(range(6))
    assert np.allclose(check_points_value, np.linspace(0, 10, 6))

    assert l.get_closest([1.01]) == [1]
    assert l.get_closest([0.99]) == [0]

    assert l.get_num_points() == 6

    assert l.get_pos_from_idx([4]) == [8]

    assert l.get_shape() == [6]

    assert l.max_node_pos == [10]
    assert l.min_node_pos == [0]

    assert l.min_max_num_list == [[0, 10, 6]]
    assert l.order == 'F'
    assert l.nodes == [6]
    assert str(l) == "Lattice([[0, 10, 6]])"
    assert l.stepsizes == [2]

    assert np.allclose(l.get_positions()[:, 0], np.linspace(0, 10, 6))


def test_lattice_object_1d_scales():
    l = lattice.Lattice([[0, 10, 6]])
    assert l.dim == 1

    l.scale(0.5)

    assert l.max_node_pos == [5]
    assert l.stepsizes == [1]

    l.scale(1 / 0.5)
    assert l.max_node_pos == [10]
    assert l.stepsizes == [2]


def test_lattice_object_2d():
    l = lattice.Lattice([[0, 10, 6], [-3, 1, 2]])
    assert l.dim == 2

    check_points_index = []
    check_points_value = []

    def f(idx, x):
        print("idx = {} x={}".format(idx, x))
        check_points_index.append(idx[:])
        check_points_value.append(x[:])

    l.foreach(f)

    assert check_points_index == [[0, 0],
                                  [1, 0],
                                  [2, 0],
                                  [3, 0],
                                  [4, 0],
                                  [5, 0],
                                  [0, 1],
                                  [1, 1],
                                  [2, 1],
                                  [3, 1],
                                  [4, 1],
                                  [5, 1]]
    assert np.allclose(check_points_value, [[0.0, -3.0],
                                            [2.0, -3.0],
                                            [4.0, -3.0],
                                            [6.0, -3.0],
                                            [8.0, -3.0],
                                            [10.0, -3.0],
                                            [0.0, 1.0],
                                            [2.0, 1.0],
                                            [4.0, 1.0],
                                            [6.0, 1.0],
                                            [8.0, 1.0],
                                            [10.0, 1.0]])

    assert l.get_closest([1.01, -0.9]) == [1, 1]
    assert l.get_closest([1.01, -1.0001]) == [1, 0]
    assert l.get_num_points() == 12

    assert l.dim == 2

    with pytest.raises(IndexError):
        l.get_pos_from_idx([1])  # should raise IndexError for 2d mesh

    l.get_pos_from_idx([0, 0]) == [0., -3.]
    l.get_pos_from_idx([0, 1]) == [0., 1.]
    l.get_pos_from_idx([4, 1]) == [8., 1.]

    assert l.get_shape() == [6, 2]

    l.max_node_pos == [10, 1]

    assert l.min_max_num_list == [[0, 10, 6], [-3, 1, 2]]
    assert l.min_node_pos == [0, -3]
    assert l.nodes == [6, 2]
    assert l.order == 'F'
    assert str(l) == "Lattice([[0, 10, 6], [-3, 1, 2]])"

    assert np.allclose(l.get_positions(),
                       np.array([[[0., -3.],
                                  [2., -3.],
                                  [4., -3.],
                                  [6., -3.],
                                  [8., -3.],
                                  [10., -3.]],
                                 [[0., 1.],
                                  [2., 1.],
                                  [4., 1.],
                                  [6., 1.],
                                  [8., 1.],
                                  [10., 1.]]]))


def test_lattice_object_2d_scale():

    l = lattice.Lattice([[0, 10, 6], [-3, 1, 2]])
    assert l.dim == 2

    l.scale(2)
    assert l.max_node_pos == [20, 2]
    assert l.stepsizes == [4, 8]

    l.scale(0.5)
    assert l.max_node_pos == [10, 1]
    assert l.stepsizes == [2, 4]


def test_field_lattice_init():
    fl = lattice.FieldLattice(lattice.Lattice([[0, 10, 6], [-3, 1, 2]]))

    # we want to see numpy.ndarray for the data
    assert type(fl.field_data) == np.ndarray
    # and contiguous data
    assert fl.field_data.flags['F_CONTIGUOUS'] is True
    # and the right shape
    assert fl.field_data.shape[1:] == tuple(fl.lattice.get_shape())
    # and 3d data vectors
    assert fl.field_data.shape[0] == 3 == fl.field_dim
    # but the lattice is in 2d only
    assert fl.lattice.dim == 2


def test_field_lattice_set():
    z_counter = [0]  # cheat to see in which order field vaules are set

    def mydata(pos):
        print("type of pos = {}".format(type(pos)))
        print("pos = {}".format(pos))
        # use position as field data (for our testing here)
        x, y = pos
        z = z_counter[0]
        z_counter[0] += 0.1
        return [x, y, z]

    fl = lattice.FieldLattice(lattice.Lattice([[0, 5, 6], [-2, -1, 2]]))
    fl.set(mydata)
    print(fl.field_data.shape)
    print(fl.field_data[:, :, :])
    print("==============")
    print(fl.field_data[2, :, :])
    print(np.array([np.linspace(0, 1.1, 12)]))
    print("==============")

    # check x-component
    assert np.allclose(fl.field_data[0, :, :],
                       np.array([[0., 0.],
                                 [1., 1.],
                                 [2., 2.],
                                 [3., 3.],
                                 [4., 4.],
                                 [5., 5.]]))

    # check y-component
    assert np.allclose(fl.field_data[1, :, :],
                       np.array([[-2., -1.],
                                 [-2., -1.],
                                 [-2., -1.],
                                 [-2., -1.],
                                 [-2., -1.],
                                 [-2., -1.]]))

    # check z-component in Fortran ordering
    assert np.allclose(fl.field_data[2, :, :],
                       np.array([[0.0, 0.6],
                                 [0.1, 0.7],
                                 [0.2, 0.8],
                                 [0.3, 0.9],
                                 [0.4, 1.0],
                                 [0.5, 1.1]]))

    # How does C order differ?
    # Okay, simplify: establish only that C-order is different from F-order:
    flf = fl  # FieldLattice Fortran

    # Create FieldLattice C with identical data
    flc = lattice.FieldLattice(lattice.Lattice([[0, 5, 6], [-2, -1, 2]]),
                               order="C")
    z_counter[0] = 0
    fl.set(mydata)

    # compare values (should be the same)
    assert np.allclose(flc.field_data, flf.field_data)

    # check that the strides are different (check help(numpy.ndarray))
    assert flc.field_data.strides != flf.field_data.strides
