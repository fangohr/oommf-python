import numpy as np
import matplotlib.pyplot as plt


class VectorField(object):
    def __init__(self, filename):
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            if line.startswith('# xmin'):
                self.xmin = float(line[7:])
            if line.startswith('# ymin'):
                self.ymin = float(line[7:])
            if line.startswith('# zmin'):
                self.zmin = float(line[7:])
            if line.startswith('# xmax'):
                self.xmax = float(line[7:])
            if line.startswith('# ymax'):
                self.ymax = float(line[7:])
            if line.startswith('# zmax'):
                self.zmax = float(line[7:])
            if line.startswith('# xstepsize'):
                self.dx = float(line[12:])
            if line.startswith('# ystepsize'):
                self.dy = float(line[12:])
            if line.startswith('# zstepsize'):
                self.dz = float(line[12:])
            if line.startswith('# xnodes'):
                self.nx = int(line[9:])
            if line.startswith('# ynodes'):
                self.ny = int(line[9:])
            if line.startswith('# znodes'):
                self.nz = int(line[9:])

        self.coords = np.zeros([self.nx*self.ny*self.nz, 3])
        self.x_array = np.arange(self.xmin+self.dx/2., self.xmax, self.dx)
        self.y_array = np.arange(self.ymin+self.dy/2., self.ymax, self.dy)
        self.z_array = np.arange(self.zmin+self.dz/2., self.zmax, self.dz)

        counter = 0
        for z in self.z_array:
            for y in self.y_array:
                for x in self.x_array:
                    self.coords[counter, :] = [x, y, z]
                    counter += 1

        self.vf = np.zeros([self.nx*self.ny*self.nz, 3])
        counter = 0
        for line in lines:
            if not line.startswith('#'):
                parts = line.split()
                self.vf[counter, 0] = float(parts[0])
                self.vf[counter, 1] = float(parts[1])
                self.vf[counter, 2] = float(parts[2])
                counter += 1

    def find_nearest(self, value, array):
        difference = np.abs(array - value)
        return array[difference.argmin()]

    def get_coords(self):
        return self.coords

    def get_vf(self):
        return self.vf

    def get_index(self, coord):
        x = self.find_nearest(coord[0], self.x_array)
        y = self.find_nearest(coord[1], self.y_array)
        z = self.find_nearest(coord[2], self.z_array)
        counter = 0
        for i in range(self.nx*self.ny*self.nz):
            if self.coords[i, 0] == x and self.coords[i, 1] == y and \
               self.coords[i, 2] == z:
                return counter
            counter += 1
    
    def sample(self, coord):
        x = self.find_nearest(coord[0], self.x_array)
        y = self.find_nearest(coord[1], self.y_array)
        z = self.find_nearest(coord[2], self.z_array)
        return self.vf[self.get_index((x, y, z)), :]

    def z_slice(self, z):
        slice_coords = np.zeros([self.nx*self.ny, 2])
        slice_vf = np.zeros([self.nx*self.ny, 3])
        counter = 0
        for y in self.y_array:
            for x in self.x_array:
                slice_coords[counter, :] = [x, y]
                slice_vf[counter, :] = self.sample((x, y, z))
                counter += 1
        return slice_coords, slice_vf

    def plot_z_slice(self, z):
        slice_coords, slice_vf = self.z_slice(z)
        plt.quiver(slice_coords[:, 0]/1e-9, slice_coords[:, 1]/1e-9,
                   slice_vf[:, 0], slice_vf[:, 1])
        plt.xlabel('x (nm)')
        plt.ylabel('y (nm)')
        plt.grid()
        plt.show()

    def average(self):
        return (np.mean(self.vf[:, 0]), np.mean(self.vf[:, 1]), np.mean(self.vf[:, 2]))
