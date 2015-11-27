class Sim(object):
    def __init__(self, mesh, Ms):
        self.mesh = mesh
        self.Ms = Ms
        self.energies = []

    def add_exchange(self, A):
        self.energies.append(('Exchange', A))

    def add_demag(self):
        self.energies.append(('Demag', None))

    def add_zeeman(self, H):
        self.energies.append(('Zeeman', H))

    def set_m(self, m_init):
        self.m_init = m_init

    def create_mif(self):
        pass

    def run_until(self, t_sim):
        pass

    def result(self):
        pass
