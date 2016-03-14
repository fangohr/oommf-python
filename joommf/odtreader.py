"""
odtreader.py

Contains class ODTFile for reading OOMMF ODT data into a Pandas dataframe

Author: Ryan Pepper (2016)

University of Southampton
"""

import pandas as pd
import tempfile
import re


class ODTFile(object):

    def __init__(self, filename):
        f = open(filename)
# Can't use 'w+b' for compatibility with Py2
        temporary_file = tempfile.NamedTemporaryFile(mode='w')

        metadata = []
        for line in f:
            if line[0] == '#':
                metadata.append(line)
            else:
                new_line = re.sub(r'\s+', ',', line.lstrip().rstrip()) + '\n'
                temporary_file.write(new_line)
        temporary_file.flush()
        self.dataframe = pd.read_csv(temporary_file.name, header=None)
        header = []
        for column in metadata[3].split('Oxs_')[1:]:
            column = column.replace('{', '')
            column = column.replace('}', '')
            column = column.rstrip().replace(' ', '_')
            column = column.replace('::', '_')
            column = column.replace(':', '_')
            column = column.replace('RungeKuttaEvolve_evolve_', '')
            column = column.replace('TimeDriver_', '')
            column = column.replace('Simulation_', '')
            header.append(column)
        self.dataframe.columns = header
        temporary_file.close()
        self.df = self.dataframe
