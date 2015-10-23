class Geometry(object):
    def __init__(self, name="geometry", unitlength=1):
        pass
        self.name = name
        self.unitlength = unitlength
    
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.__repr__()
    


class Cuboid(Geometry):
    def __init__(self, corner1, corner2, unitlength):
        pass
        self.corner1 = corner1
        self.corner2 = corner2
        super(Cuboid, self).__init__(name="Cuboid", unitlength=unitlength)

    def __repr__(self):
        desc = "corner1 = {}, corner2 = {}".format(self.corner1, self.corner2)
        return super(Cuboid, self).__repr__() + " " + desc

    def __str__(self):
        return self.__repr__()
    
    def get_cells(self, cellsize):
        try:
            assert len(cellsize) == 3
        except TypeError:
            # assume it is a scalar
            cellsize = cellsize, cellsize, cellsize

        volx = (self.corner2[0] - self.corner1[0]) * self.unitlength
        voly = (self.corner2[1] - self.corner1[1]) * self.unitlength
        volz = (self.corner2[2] - self.corner1[2]) * self.unitlength

        ns = [ int(v//cs) for cs, v in zip(cellsize, [volx, voly, volz])]
        return ns

if __name__ == "__main__":
    cube = Cuboid((0,0,0), (1,2,3))
    print(repr(cube))
