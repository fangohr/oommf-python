import textwrap


class Mesh(object):
    """class Mesh(lengths, mesh_spacing, scale=1e-9)
       lengths: list
            List of 3 lengths which make up the global atlas
       mesh_spacing:
            List of 3 discretisations.

       Example usage:
       For a rectangular block of 30x30x50nm, with mesh nodes
       every 5nm, create a Mesh object with
       mesh = Mesh([30, 30, 50], [5, 5, 5])
       """

    def __init__(self, lengths, mesh_spacing, scale=1e-9):
        assert len(lengths) == 3, "Lengths must contain three values"
        assert len(mesh_spacing) == 3, "mesh_spacing must contain a value" + \
            "for each coordinate direction"
        components = ['x', 'y', 'z']
        for vals, component in zip(lengths, components):
            assert vals > 0, 'L component {} must be a positive value'.format(
                component)
        self.lx = lengths[0]
        self.ly = lengths[1]
        self.lz = lengths[2]
        self.dx = mesh_spacing[0]
        self.dy = mesh_spacing[1]
        self.dz = mesh_spacing[2]
        self.scale = scale

    def mesh_info(self):
        return (self.lx, self.ly, self.lz, self.dx, self.dy, self.dz)

    def _atlas_mif(self):
        atlas_mif = textwrap.dedent("""\
            Specify Oxs_BoxAtlas:atlas {{
                 xrange {{0 {}}}
                 yrange {{0 {}}}
                 zrange {{0 {}}}
             }}
             """).format(self.lx, self.ly, self.lz)
        return atlas_mif

    def _mesh_mif(self):
        mesh_mif = 'Specify Oxs_RectangularMesh:mesh {\n'
        mesh_mif += '\tcellsize {%2e %2e %2e}\n' % (self.dx, self.dy, self.dz)
        mesh_mif += '\tatlas :atlas\n'
        mesh_mif += '}\n\n'
        return mesh_mif

    def get_mif(self):
        return self._atlas_mif() + self._mesh_mif()
