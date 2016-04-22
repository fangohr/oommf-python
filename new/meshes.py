class RectangularMesh(object):
    def __init__(self, d, atlas, meshname='mesh'):
        if not isinstance(d, (tuple, list)) or len(d) != 3:
            raise ValueError('Cellsize d must be a tuple of length 3.')
        elif d[0] <= 0 or d[1] <= 0 or d[2] <= 0:
            raise ValueError('Cellsize dimensions must be positive.')
        else:
            self.d = d

        if not isinstance(atlas, str):
            raise ValueError('atlas must be a string.')
        else:
            self.atlas = atlas

        if not isinstance(meshname, str):
            raise ValueError('name must be a string.')
        else:
            self.meshname = meshname

    def get_mif(self):
        data = [('xstep', self.d[0]),
                ('ystep', self.d[1]),
                ('zstep', self.d[2])]

        # Create mif string.
        mif = '# RectangularMesh\n'
        for datum in data:
            mif += 'set {} {}\n'.format(datum[0], datum[1])
        mif += 'Specify Oxs_RectangularMesh:{}'.format(self.meshname) + ' {\n'
        mif += '\tcellsize { $xstep $ystep $zstep }\n'
        mif += '\tatlas {}\n'.format(self.atlas)
        mif += '}\n\n'

        return mif
