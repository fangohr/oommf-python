class BoxAtlas(object):
    def __init__(self, cmin, cmax, atlasname='atlas',
                 regionname='regionname'):
        if cmin[0] >= cmax[0] or cmin[1] >= cmax[1] or cmin[2] >= cmax[2]:
            raise ValueError('Values in cmin should be smaller tha cmax.')
        else:
            self.cmin = cmin
            self.cmax = cmax

        if not isinstance(atlasname, str):
            raise ValueError('atlasname must be a string.')
        else:
            self.atlasname = atlasname

        if not isinstance(regionname, str):
            raise ValueError('regionname must be a string.')
        else:
            self.regionname = regionname

    def get_mif(self):
        data = [('xmin', self.cmin[0]),
                ('ymin', self.cmin[1]),
                ('zmin', self.cmin[2]),
                ('xmax', self.cmax[0]),
                ('ymax', self.cmax[1]),
                ('zmax', self.cmax[2])]

        # Create mif string.
        mif = '# BoxAtlas\n'
        for datum in data:
            mif += 'set {} {}\n'.format(datum[0], datum[1])
        mif += 'Specify Oxs_BoxAtlas:{}'.format(self.atlasname) + ' {\n'
        mif += '\txrange { $xmin $xmax }\n'
        mif += '\tyrange { $ymin $ymax }\n'
        mif += '\tzrange { $zmin $zmax }\n'
        mif += '\tname {}\n'.format(self.regionname)
        mif += '}\n\n'

        return mif
