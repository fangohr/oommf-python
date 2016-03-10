"""
odtreader.py

Contains class ODTFile for reading OOMMF ODT data into a Pandas dataframe

Author: Ryan Pepper (2016)

University of Southampton
"""

import pandas as pd
import numpy as np


class ODTFile(object):

    def __init__(self, filename):
        f = open(filename)
        self._raw_linedata = f.read().split("\n")
        f.close()
        # Set up temporary data structures
        self._raw_metadata = []

        self.headers = []
        self._header_indices = []
        # Here we just select the lines that are the headers,
        # so that we can retrieve information
        # about the data stored in the ODT file.
        for index, line in enumerate(self._raw_linedata):
            if '#' not in line:
                break
            else:
                self._raw_metadata.append(line)
                # Do this so we can skip later.
                self._header_indices.append(index)
        for line in self._raw_metadata:
            if 'ODT' in line:
                self.odt_version = line.split()[2]  # Grab ODT File version
            if 'Title' in line:
                # Grab date string from ODT file
                self.sim_date = line.split(',')[1]

        # These next few lines get the data for the headers.
            if 'Columns:' in line:
                headers = []
            # Have to use this as the split because of spaces in some column
            # headers.
                for i, line in enumerate(line.split('Oxs')):
                    if i != 0:
                        headers.append(
                            line.replace('_', '').replace(
                                '}', '').replace(
                                '{', '').rstrip())
            if 'Units:' in line:
                raw_units = line.split()[2:]
        # Construct headers from data -need to add units if they exist.
        # If they don't have units, it's represented by {} in ODT file.
        for header, unit in zip(headers, raw_units):
            if unit != '{}':
                self.headers.append(header + ' (' + unit + ')')
            else:
                self.headers.append(header)
        # Skip the final line as this just contains # End Table
        N_lines = len(self._raw_linedata) - len(self._header_indices) - 2
        # Preallocate data for the dataframe to save time
        self.dataframe = pd.DataFrame(
            index=np.arange(0, N_lines), columns=headers)
        for index, line in enumerate(self._raw_linedata[len(
                self._header_indices):N_lines]):
            try:
                split_line = [float(i) for i in line.split()]
                self.dataframe.loc[index] = split_line
            except ValueError:
                print("Failed to read line:\n{}".format(line))
