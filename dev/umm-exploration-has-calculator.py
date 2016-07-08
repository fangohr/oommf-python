class MicromagneticModell:
    def __init__(self, name, Ms, calc):
        self.name = name
        self.Ms = Ms
        self.field = None
        self.calc = calc

    def __str__(self):
        return "AbstractMicromagneticModell(name={})".format(self.name)

    def relax(self):
        self.calc.relax(self)

    def set_H(self, field):
        print("AbstractMicromagneticModell: setting field = {}")
        self.field = field

    def hysteresis(self, fieldlist):
        print("AbstractMicromagneticModell: starting hysteresis")
        for field in fieldlist:
            self.set_H(field)
            self.relax()

class OOMMFC():

    def __init__(self):
        pass

    def __str__(self):
        return "OOMMFC()"

    def relax(self, mm):
        print("Calling OOMMF to run relax() with H={}".format(mm.field))


#a = AbstractMicromagneticModell('simulation-name', 10)


#print(a)
#a.hysteresis([10, 20])

ocalc = OOMMFC()
o = MicromagneticModell(name='test', Ms=42, calc=ocalc)
print(o)
o.relax()

#f = FIDIMAGC(name='fidimag-simulation', Ms=8e6)
#print(o)
#f.relax()

#o.relax()
#o.hysteresis([10, 20, 30])
