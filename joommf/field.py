import random
import numpy as np
import matplotlib.pyplot as plt


class Field(object):
    def __init__(self, cmin, cmax, d, dim=1, value=None, name=None):
        self.cmin = cmin
        self.cmax = cmax
        self.d = d
        self.dim = dim
        self.name = name

        # Compute domain edge lengths.
        self.l = (self.cmax[0]-self.cmin[0],
                  self.cmax[1]-self.cmin[1],
                  self.cmax[2]-self.cmin[2])

        # Compute the number of cells in x, y, and z directions.
        tol = 1e-12
        if (self.d[0] - tol > self.l[0] % self.d[0] > tol) or
        (self.d[1] - tol > self.l[1] % self.d[1] > tol) or
        (self.d[2] - tol > self.l[2] % self.d[2] > tol):
            raise ValueError('Domain is not a multiple of {}.'.format(self.d))

        else:
            self.n = (int(round(self.l[0]/self.d[0])),
                      int(round(self.l[1]/self.d[1])),
                      int(round(self.l[2]/self.d[2])))

        # Create an empty 3d vector field.
        self.f = np.zeros([self.n[0], self.n[1], self.n[2], dim])

        if value is not None:
            self.set(value)

    def __call__(self, c):
        return self.sample(c)

    def domain_centre(self):
        c = (self.cmin[0] + 0.5*self.l[0],
             self.cmin[1] + 0.5*self.l[1],
             self.cmin[2] + 0.5*self.l[2])

        return c

    def random_coord(self):
        c = (self.cmin[0] + random.random()*self.l[0],
             self.cmin[1] + random.random()*self.l[1],
             self.cmin[2] + random.random()*self.l[2])

        return c

    def index2coord(self, i):
        if i[0] < 0 or i[0] > self.n[0]-1 or \
           i[1] < 0 or i[1] > self.n[1]-1 or \
           i[2] < 0 or i[2] > self.n[2]-1:
            raise ValueError('Index {} out of range.'.format(i))

        else:
            c = (self.cmin[0] + (i[0] + 0.5)*self.d[0],
                 self.cmin[1] + (i[1] + 0.5)*self.d[1],
                 self.cmin[2] + (i[2] + 0.5)*self.d[2])

        return c

    def coord2index(self, c):
        if c[0] < self.cmin[0] or c[0] > self.cmax[0] or
        c[1] < self.cmin[1] or c[1] > self.cmax[1] or
        c[2] < self.cmin[2] or c[2] > self.cmax[2]:
            raise ValueError('Coordinate {} out of domain.'. format(c))

        else:
            i = [int(round(float(c[0]-self.cmin[0])/self.d[0] - 0.5)),
                 int(round(float(c[1]-self.cmin[1])/self.d[1] - 0.5)),
                 int(round(float(c[2]-self.cmin[2])/self.d[2] - 0.5))]

            # If rounded to the out-of-range index.
            for j in range(3):
                if i[j] < 0:
                    i[j] = 0
                elif i[j] > self.n[j] - 1:
                    i[j] = self.n[j] - 1

        return tuple(i)

    def nearestcellcoord(self, c):
        return self.index2coord(self.coord2index(c))

    def sample(self, c):
        i = self.coord2index(c)
        return self.f[i[0], i[1], i[2]]

    def set(self, value, normalise=False):
        if isinstance(value, (int, float)):
            self.f.fill(value)

        elif isinstance(value, (tuple, list, np.ndarray)):
            for i in range(self.dim):
                self.f[:, :, :, i].fill(value[i])

        elif hasattr(value, '__call__'):
            for ix in xrange(self.n[0]):
                for iy in xrange(self.n[1]):
                    for iz in xrange(self.n[2]):
                        i = (ix, iy, iz)
                        coord = self.index2coord((ix, iy, iz))
                        self.f[ix, iy, iz, :] = value(coord)

        else:
            raise TypeError("Cannot set field using {}.".format(type(value)))

        if normalise:
            self.normalise()

    def set_at_index(self, i, value):
        self.f[i[0], i[1], i[2], :] = value

    def slice_field(self, axis, point):
        if axis == 'x':
            slice_num = 0
            axes = (1, 2)
        elif axis == 'y':
            slice_num = 1
            axes = (0, 2)
        elif axis == 'z':
            slice_num = 2
            axes = (0, 1)
        else:
            raise ValueError('Axis not properly defined.')

        if self.cmin[slice_num] <= point <= self.cmax[slice_num]:
            axis1_indices = np.arange(0, self.n[axes[0]])
            axis2_indices = np.arange(0, self.n[axes[1]])

            axis1_coords = np.zeros(len(axis1_indices))
            axis2_coords = np.zeros(len(axis2_indices))

            sample_centre = list(self.domain_centre())
            sample_centre[slice_num] = point
            sample_centre = tuple(sample_centre)

            slice_index = self.coord2index(sample_centre)[slice_num]

            field_slice = np.zeros([self.n[axes[0]],
                                    self.n[axes[1]],
                                    self.dim])
            for j in axis1_indices:
                for k in axis2_indices:
                    i = [0, 0, 0]
                    i[slice_num] = slice_index
                    i[axes[0]] = j
                    i[axes[1]] = k
                    i = tuple(i)

                    coord = self.index2coord(i)

                    axis1_coords[j] = coord[axes[0]]
                    axis2_coords[k] = coord[axes[1]]

                    field_slice[j, k, :] = self.f[i[0], i[1], i[2], :]
            coord_system = (axes[0], axes[1], slice_num)

        else:
            raise ValueError('Point {} outside the domain.'.format(point))

        return axis1_coords, axis2_coords, field_slice, coord_system

    def plot_slice(self, axis, point):
        a1, a2, field_slice, coord_system = self.slice_field(axis, point)

        if self.dim == 1:
            plt.imshow(field_slice[:, :, 0],
                       extent=[a1[0], a1[-1], a2[0], a2[-1]],
                       aspect='auto')

        elif self.dim == 3:
            pm = self._prepare_for_quiver(a1, a2,
                                          field_slice,
                                          coord_system)

            if np.allclose(pm[:, 2], 0) and np.allclose(pm[:, 3], 0):
                raise ValueError('Vector plane components are zero.')
            else:
                plt.quiver(pm[:, 0], pm[:, 1], pm[:, 2], pm[:, 3], pm[:, 4])
                plt.xlim([self.cmin[coord_system[0]],
                          self.cmax[coord_system[0]]])
                plt.ylim([self.cmin[coord_system[1]],
                          self.cmax[coord_system[1]]])
                plt.xlabel('xyz'[coord_system[0]])
                plt.ylabel('xyz'[coord_system[1]])
                plt.title('xyz'[coord_system[2]] + ' slice')
                plt.grid()
                plt.show()

    def _prepare_for_quiver(self, a1, a2, field_slice, coord_system):
        nel = self.n[coord_system[0]]*self.n[coord_system[1]]
        plot_matrix = np.zeros([nel, 5])

        counter = 0
        for j in xrange(self.n[coord_system[0]]):
            for k in xrange(self.n[coord_system[1]]):
                entry = [a1[j], a2[k],
                         field_slice[j, k, coord_system[0]],
                         field_slice[j, k, coord_system[1]],
                         field_slice[j, k, coord_system[2]]]
                plot_matrix[counter, :] = np.array(entry)
                counter += 1

        return plot_matrix

    def normalise(self, norm=1):
        if self.dim == 1:
            raise NotImplementedError("""Normalisation of scalar
                                      fields is not implemented.""")

        else:
            # Compute norm.
            f_norm = 0
            for j in range(self.dim):
                f_norm += self.f[:, :, :, j]**2
            f_norm = np.sqrt(f_norm)

            # Normalise every component.
            for j in range(self.dim):
                self.f[:, :, :, j] = norm * self.f[:, :, :, j]/f_norm


def load_oommf_file(filename, name=None):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    # Load metadata.
    dic = {'xmin': None, 'ymin': None, 'zmin': None,
           'xmax': None, 'ymax': None, 'zmax': None,
           'xstepsize': None, 'ystepsize': None, 'zstepsize': None,
           'xbase': None, 'ybase': None, 'zbase': None,
           'xnodes': None, 'ynodes': None, 'znodes': None,
           'valuedim': None}

    for line in lines[0:50]:
        for key in dic.keys():
            if line.find(key) != -1:
                dic[key] = float(line.split()[2])

    cmin = (dic['xmin'], dic['ymin'], dic['zmin'])
    cmax = (dic['xmax'], dic['ymax'], dic['zmax'])
    d = (dic['xstepsize'], dic['ystepsize'], dic['zstepsize'])
    cbase = (dic['xbase'], dic['ybase'], dic['zbase'])
    n = (int(round(dic['xnodes'])),
         int(round(dic['ynodes'])),
         int(round(dic['znodes'])))
    dim = int(dic['valuedim'])

    field = Field(cmin, cmax, d, dim, name=name)

    for j in xrange(len(lines)):
        if lines[j].find('Begin: Data') != -1:
            data_first_line = j+1

    counter = 0
    for ix in xrange(n[0]):
            for iy in xrange(n[1]):
                    for iz in xrange(n[2]):
                        i = (ix, iy, iz)
                        line_data = lines[data_first_line+counter]
                        value = [float(vi) for vi in line_data.split()]
                        field.set_at_index(i, value)

                        counter += 1
