class AbstractMicromagneticModell:
    def __init__(self, name, Ms):
        self.name = name
        self.Ms = Ms
        self.field = None
        self.energies = []

    def __str__(self):
        return "AbstractMicromagneticModell(name={})".format(self.name)

    def relax(self):
        self._relax()
        #raise NotImplementedError("relax is abstract method")

    def set_H(self, field):
        print("AbstractMicromagneticModell: setting field = {}")
        self.field = field

    def hysteresis(self, fieldlist):
        print("AbstractMicromagneticModell: starting hysteresis")
        for field in fieldlist:
            self.set_H(field)
            self._relax()


class OOMMFC(AbstractMicromagneticModell):

    def __init__(self, name, Ms):
        AbstractMicromagneticModell.__init__(self, name, Ms)

    def __str__(self):
        return "OOMMFC(name={}, Ms={})".format(self.name, self.Ms)

    def _relax(self):
        print("Calling OOMMF to run relax() with H={}".format(self.field))

class FIDIMAGC(AbstractMicromagneticModell):

    def __init__(self, name, Ms):
        AbstractMicromagneticModell.__init__(self, name, Ms)

    def __str__(self):
        return "FIDIMAG(name={}, Ms={})".format(self.name, self.Ms)

    def _relax(self):
        print("Calling FIDIMAG to run relax() with H={}".format(self.field))


#a = AbstractMicromagneticModell('simulation-name', 10)


#print(a)
#a.hysteresis([10, 20])

o = OOMMFC(name='oommf-simulation', Ms=8e6)
print(o)
o.relax()

f = FIDIMAGC(name='fidimag-simulation', Ms=8e6)
print(o)
f.relax()

#o.relax()
#o.hysteresis([10, 20, 30])
