import pytest
from meshes import RectangularMesh


class TestRectangularMesh(object):
    def setup(self):
        # Set of valid arguments.
        self.args1 = [[(1, 1, 1), 'atlas1', 'mesh1'],
                      [(1e-9, 1e-9, 1e-9), 'atlas2', 'mesh2'],
                      [(5, 1, 1e-9), 'atlas3', 'mesh3'],
                      [(1.0, 13-6, 1.1e4), 'atlas4', 'mesh4']]

        # Set of invalid arguments.
        self.args2 = [[(0, 1, 1), 'atlas1', 'mesh1'],
                      [(1, -0.1e-9, 1e-9), 'atlas2', 'mesh2'],
                      [(5, 1, 1e-9), 7, 'mesh3'],
                      [(1.0, 13-6, 1.1e4), 'atlas4', [1, 2]]]

    def test_init(self):
        # Valid arguments.
        for arg in self.args1:
            d = arg[0]
            atlas = arg[1]
            meshname = arg[2]

            mesh = RectangularMesh(d, atlas, meshname)

            assert mesh.d == d
            assert mesh.atlas == atlas
            assert mesh.meshname == meshname

            assert isinstance(mesh.d, tuple)
            assert isinstance(mesh.atlas, str)
            assert isinstance(mesh.meshname, str)

    def test_init_exceptions(self):
        # Invalid arguments (ValueError expected).
        for arg in self.args2:
            with pytest.raises(ValueError):
                d = arg[0]
                atlas = arg[1]
                meshname = arg[2]

                mesh = RectangularMesh(d, atlas, meshname)

    def test_get_mif(self):
        for arg in self.args1:
            d = arg[0]
            atlas = arg[1]
            meshname = arg[2]

            mesh = RectangularMesh(d, atlas, meshname)

            mif = mesh.get_mif()
            mif_lines = mesh.get_mif().split('\n')

            # Assert comment.
            l = mif_lines[0].split()
            assert l[0] == '#'
            assert l[1] == 'RectangularMesh'

            # Assert Specify line.
            l = mif_lines[1].split()
            assert l[0] == 'Specify'
            assert l[1].split(':')[0] == 'Oxs_RectangularMesh'
            assert l[1].split(':')[1] == meshname
            assert l[2] == '{'

            # Assert step line.
            assert mif_lines[2][0] == '\t'
            l = mif_lines[2].split()
            assert l[0] == 'cellsize'
            assert l[1] == '{'
            assert float(l[2]) == d[0]
            assert float(l[3]) == d[1]
            assert float(l[4]) == d[2]
            assert l[5] == '}'

            # Assert atlas name.
            assert mif_lines[3][0] == '\t'
            l = mif_lines[3].split()
            assert l[0] == 'atlas'
            assert l[1] == atlas

            # Assert mif end.
            assert mif_lines[4] == '}'

            # Assert new lines at the end of the string.
            assert mif[-2:] == '\n\n'
