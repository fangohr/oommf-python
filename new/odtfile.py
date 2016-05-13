import pandas as pd
import numpy as np


class ODTFile(object):
    def __init__(self, odt_filename):
        f = open(odt_filename)
        lines = f.readlines()
        f.close()
        
        for i in range(len(lines)):
            if lines[i].startswith('# Columns:'):
                columns_line = i
                line = lines[i]
                parts = line.split('Oxs_')[1:]
                self.header = []
                for part in parts:
                    tmp_string = part
                    tmp_string = tmp_string.replace('{', '')
                    tmp_string = tmp_string.replace('}', '')
                    tmp_string = tmp_string.replace('RungeKuttaEvolve:evolver:', '')
                    tmp_string = tmp_string.replace('TimeDriver::', '')
                    tmp_string = tmp_string.replace('FixedZeeman:fixedzeeman:', '')
                    tmp_string = tmp_string.replace('TimeDriver', '')
                    tmp_string = tmp_string.replace('Uniform', '')
                    tmp_string = tmp_string.replace(' ', '')
                    tmp_string = tmp_string.replace('::', '')
                    tmp_string = tmp_string.replace('\n', '')
                    tmp_string = tmp_string.replace('CGEvolve:evolver:', '')
                    self.header.append(tmp_string)
        
        self.data = []
        for i in range(columns_line, len(lines)):
            line = lines[i]
            if line[0] != '#':
                data_line = []
                numbers = line.split()
                for number in numbers:
                    data_line.append(float(number))
                self.data.append(data_line)

        self.df = pd.DataFrame(self.data, columns=self.header)

    def last_row(self):
        return self.df.loc[self.df.index[-1]]
