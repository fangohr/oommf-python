class energy(object):

    def __init__(self, energy_type):
        """
        Base energy class
        """
        self.type = energy_type

    def __repr__(self):
        return "This is the energy class of type {}".format(self.type)
