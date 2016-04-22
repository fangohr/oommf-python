import random
import numpy as np
from field import Field

class TestField(object):
    def setup(self):
        self.scalar_fs = self.create_scalar_fs()
        self.vector_fs = self.create_vector_fs()
        self.constant_values = [0, -5., np.pi,
                                1e-15, 1.2e12, random.random()]
        self.tuple_values = [(0, 0, 1),
                             (0, -5.1, np.pi),
                             [70, 1e15, 2*np.pi],
                             [5, random.random(), np.pi],
                             np.array([4, -1, 3.7]),
                             np.array([2.1, 0.0, -5*random.random()])]
        self.scalar_pyfuncs = self.create_scalar_pyfuncs()
        self.vector_pyfuncs = self.create_vector_pyfuncs()

    def create_scalar_fs(self):
        cmin_list = [(0, 0, 0), (-5, -8, -10), (10, -5, -80)]
        cmax_list = [(5, 8, 10), (11, 4, 4), (15, 10, 85)]
        d_list = [(1, 1, 1), (1, 2, 1), (5, 5, 2.5)]

        scalar_fs = []
        for i in range(len(cmin_list)):
            f = Field(cmin_list[i], cmax_list[i], d_list[i], 1)
            scalar_fs.append(f)

        return scalar_fs

    def create_vector_fs(self):
        cmin_list = [(0, 0, 0), (-5, -8, -10), (10, -5, -80)]
        cmax_list = [(5, 8, 10), (11, 4, 4), (15, 10, 85)]
        d_list = [(1, 1, 1), (1, 2, 1), (5, 5, 2.5)]

        vector_fs = []
        for i in range(len(cmin_list)):
            f = Field(cmin_list[i], cmax_list[i], d_list[i], 3)
            vector_fs.append(f)

        return vector_fs

    def create_scalar_pyfuncs(self):
        f1 = lambda c: 1
        f2 = lambda c: -2.4
        f3 = lambda c: -6.4e-15
        f4 = lambda c: c[0] + c[1] + c[2] + 1
        f5 = lambda c: (c[0]-1)**2 - c[1]+7 + c[2]*0.1
        f6 = lambda c: np.sin(c[0]) + np.cos(c[1]) - np.sin(2*c[2])

        return [f1, f2, f3, f4, f5, f6]

    def create_vector_pyfuncs(self):
        f1 = lambda c: (1, 2, 0)
        f2 = lambda c: (-2.4, 1e-3, 9)
        f3 = lambda c: (c[0], c[1], c[2] + 100)
        f4 = lambda c: (c[0]+c[2]+10, c[1], c[2]+1)
        f5 = lambda c: (c[0]-1, c[1]+70, c[2]*0.1)
        f6 = lambda c: (np.sin(c[0]), np.cos(c[1]), -np.sin(2*c[2]))

        return [f1, f2, f3, f4, f5, f6]

    def test_init(self):
        cmin = (0, -4, 11)
        cmax = (15, 10.1, 16.5)
        d = (1, 0.1, 0.5)
        name = 'test_field'

        f = Field(cmin, cmax, d, dim=2, name=name)
    
        assert f.l[0] == 15 - 0
        assert f.l[1] == 10.1 - (-4)
        assert f.l[2] == 16.5 - 11

        assert f.n[0] == (15 - 0) / 1.0
        assert f.n[1] == (10.1 - (-4)) / 0.1
        assert f.n[2] == (16.5 - 11) / 0.5

        assert type(f.n[0]) is int
        assert type(f.n[1]) is int
        assert type(f.n[2]) is int

        assert f.name == name

        assert np.all(f.f == 0)

    def test_index2coord(self):
        cmin = (-1, -4, 11)
        cmax = (15, 10.1, 12.5)
        d = (1, 0.1, 0.5)
        name = 'test_field'

        f = Field(cmin, cmax, d, dim=2, name=name)

        assert f.index2coord((0, 0, 0)) == (-0.5, -3.95, 11.25)
        assert f.index2coord((5, 10, 1)) == (4.5, -2.95, 11.75)

    def test_coord2index(self):
        cmin = (-10, -5, 0)
        cmax = (10, 5, 10)
        d = (1, 5, 1)
        name = 'test_field'

        f = Field(cmin, cmax, d, dim=2, name=name)

        assert f.coord2index((-10, -5, 0)) == (0, 0, 0)
        assert f.n[0] == 20
        assert f.coord2index((10, 5, 10)) == (19, 1, 9)
        assert f.coord2index((0.0001, 0.0001, 5.0001)) == (10, 1, 5)
        assert f.coord2index((-0.0001, -0.0001, 4.9999)) == (9, 0, 4)

    def test_domain_centre(self):
        cmin = (-18.5, 5, 0)
        cmax = (10, 10, 10)
        d = (0.1, 0.25, 2)
        name = 'test_field'

        f = Field(cmin, cmax, d, dim=2, name=name)

        assert f.domain_centre() == (-4.25, 7.5, 5)

    def test_random_coord(self):
        cmin = (-18.5, 5, 0)
        cmax = (10, 10, 10)
        d = (0.1, 0.25, 2)
        name = 'test_field'

        f = Field(cmin, cmax, d, dim=2, name=name)

        for j in range(500):
            c = f.random_coord()
            assert f.cmin[0] <= c[0] <= f.cmax[0]
            assert f.cmin[1] <= c[1] <= f.cmax[1]
            assert f.cmin[2] <= c[2] <= f.cmax[2]

    def test_set_with_constant(self):
        for value in self.constant_values:
            for f in self.scalar_fs + self.vector_fs:
                f.set(value)

                # Check all values.
                assert np.all(f.f == value)

                # Check with sampling.
                assert np.all(f(f.random_coord()) == value)
                assert np.all(f.sample(f.random_coord()) == value)

    def test_set_with_tuple_list_ndarray(self):
        for value in self.tuple_values:
            for f in self.vector_fs:
                f.set(value)

                for j in range(3):
                    assert np.all(f.f[:, :, :, j] == value[j])
                    assert np.all(f(f.random_coord())[j] == value[j])
                    assert np.all(f.sample(f.random_coord())[j] == value[j])

    def test_set_from_callable(self):
        # Test scalar fs.
        for f in self.scalar_fs:
            for pyfun in self.scalar_pyfuncs:
                f.set(pyfun)
                
                for j in range(10):
                    c = f.random_coord()
                    expected_value = pyfun(f.nearestcellcoord(c))
                    assert f(c) == expected_value
                    assert f.sample(c) == expected_value

        # Test vector fields.
        for f in self.vector_fs:
            for pyfun in self.vector_pyfuncs:
                f.set(pyfun)

                for j in range(10):
                    c = f.random_coord()
                    expected_value = pyfun(f.nearestcellcoord(c))
                    assert np.all(f(c) == expected_value)
                    assert np.all(f.sample(c) == expected_value)
                    
    def test_slice_f(self):
        for s in 'xyz':
            for f in self.vector_fs + self.scalar_fs:
                if f.dim == 1:
                    funcs = self.scalar_pyfuncs
                elif f.dim == 3:
                    funcs = self.vector_pyfuncs

                for pyfun in funcs:
                    f.set(pyfun)
                    point = f.domain_centre()['xyz'.find(s)]
                    data = f.slice_field(s, point)
                    a1, a2, f_slice, cs = data
                    
                    if s == 'x':
                        assert cs == (1, 2, 0)
                    elif s == 'y':
                        assert cs == (0, 2, 1)
                    elif s == 'z':
                        assert cs == (0, 1, 2)

                    assert a1[0] == f.cmin[cs[0]] + f.d[cs[0]]/2.
                    assert a1[-1] == f.cmax[cs[0]] - f.d[cs[0]]/2.
                    assert a2[0] == f.cmin[cs[1]] + f.d[cs[1]]/2.
                    assert a2[-1] == f.cmax[cs[1]] - f.d[cs[1]]/2.
                    assert len(a1) == f.n[cs[0]]
                    assert len(a2) == f.n[cs[1]]
                    assert f_slice.shape == (f.n[cs[0]],
                                                 f.n[cs[1]],
                                                 f.dim)

                    for j in xrange(f.n[cs[0]]):
                        for k in xrange(f.n[cs[1]]):
                            c = list(f.domain_centre())
                            c[cs[0]] = a1[j]
                            c[cs[1]] = a2[k]
                            c = tuple(c)

                            assert np.all(f_slice[j, k] == f(c))

    def test_normalise(self):
        for f in self.vector_fs:
            for value in self.vector_pyfuncs + self.tuple_values:
                for norm_value in [1, 2.1, 50, 1e-3, np.pi]:
                    f.set(value)

                    f.normalise(norm=norm_value)

                    # Compute norm.
                    norm = 0
                    for j in range(f.dim):
                        norm += f.f[:, :, :, j]**2
                    norm = np.sqrt(norm)

                    assert norm.shape == (f.n[0], f.n[1], f.n[2])
                    diff = norm - norm_value
            
                    assert np.all(abs(norm - norm_value) < 1e-12)
