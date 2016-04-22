import pytest
from atlas import BoxAtlas


class TestBoxAtlas(object):
    def setup(self):
        # Set of valid arguments.
        self.args1 = [[(0, 0, 0), (5, 5, 5), 'atlas1', 'rn1'],
                      [(0, 0, 0), (5e-9, 5e-9, 5e-9), 'atlas2', 'rn2'],
                      [(-1.5e-9, -5e-9, 0), (1.5e-9, 15e-9, 16e-9),
                       'atlas3', 'rn3']]

        # Set of invalid arguments.
        self.args2 = [[(5, 0, 0), (0, 5, 5), 'atlas4', 'rn4'],
                      [(0, 5, 0), (5, 0, 5), 'atlas5', 'rn5'],
                      [(0, 0, 5), (5, 5, 0), 'atlas6', 'rn6'],
                      [(0, 0, 0), (5, 5, 5), 1e-9, 'rn7'],
                      [(0, 0, 0), (5, 5, 5), 'atlas', 17]]

    def test_init(self):
        # Valid arguments.
        for arg in self.args1:
            cmin = arg[0]
            cmax = arg[1]
            atlasname = arg[2]
            regionname = arg[3]

            ba = BoxAtlas(cmin, cmax, atlasname, regionname)

            assert ba.cmin == cmin
            assert ba.cmax == cmax
            assert ba.atlasname == atlasname
            assert ba.regionname == regionname

            assert isinstance(ba.cmin, tuple)
            assert isinstance(ba.cmax, tuple)
            assert isinstance(ba.atlasname, str)
            assert isinstance(ba.regionname, str)

    def test_init_exceptions(self):
        # Invalid arguments (ValueError expected).
        for arg in self.args2:
            with pytest.raises(ValueError):
                cmin = arg[0]
                cmax = arg[1]
                atlasname = arg[2]
                regionname = arg[3]

                ba = BoxAtlas(cmin, cmax, atlasname, regionname)

    def test_get_mif(self):
        for arg in self.args1:
            cmin = arg[0]
            cmax = arg[1]
            atlasname = arg[2]
            regionname = arg[3]

            ba = BoxAtlas(cmin, cmax, atlasname, regionname)

            mif = ba.get_mif()
            mif_lines = ba.get_mif().split('\n')

            # Assert comment.
            l1 = mif_lines[0].split()
            assert l1[0] == '#'
            assert l1[1] == 'BoxAtlas'

            # Assert set statements.
            expected_data = [('xmin', cmin[0]),
                             ('ymin', cmin[1]),
                             ('zmin', cmin[2]),
                             ('xmax', cmax[0]),
                             ('ymax', cmax[1]),
                             ('zmax', cmax[2])]
            c = 0
            for line in mif_lines[1:7]:
                l = line.split()
                assert l[0] == 'set'
                assert l[1] == expected_data[c][0]
                assert float(l[2]) == expected_data[c][1]
                c += 1

            # Assert Specify line.
            l = mif_lines[7].split()
            assert l[0] == 'Specify'
            assert l[1].split(':')[0] == 'Oxs_BoxAtlas'
            assert l[1].split(':')[1] == atlasname
            assert l[2] == '{'

            # Assert range lines.
            for i in range(len(mif_lines[8:11])):
                assert mif_lines[8+i][0] == '\t'
                l = mif_lines[8+i].split()
                assert l[0] == '{}range'.format('xyz'[i])
                assert l[1] == '{'
                assert l[2] == '{}min'.format('xyz'[i])
                assert l[3] == '{}max'.format('xyz'[i])
                assert l[4] == '}'

            # Assert region name.
            assert mif_lines[11][0] == '\t'
            l = mif_lines[11].split()
            assert l[0] == 'name'
            assert l[1] == regionname

            # Assert mif end.
            assert mif_lines[12] == '}'

            # Assert new lines at the end of the string.
            assert mif[-1] == '\n'
