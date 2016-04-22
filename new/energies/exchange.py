class UniformExchange(object):
    def __init__(self, A):
        if not isinstance(A, (float, int)) or A <= 0:
            raise ValueError('Exchange constant must be positive float/int.')
        else:
            self.A = A

    def get_mif(self):
        # Create mif string.
        mif = '# UniformExchange\n'
        mif += 'set A {}\n'.format(self.A)
        mif += 'Specify Oxs_UniformExchange {\n'
        mif += '\tA $A\n'
        mif += '}\n\n'

        return mif
