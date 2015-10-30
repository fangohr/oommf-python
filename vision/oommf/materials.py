class Material():

    def __init__(self, name, A):
        self.name = name
        self.A = A

    def __repr__(self):
        return self.name

permalloy = Material(name='Py(Fe80Ni20)', A=13.0e-12)
#NiFe = Material(name = 'NiFe', A=)
