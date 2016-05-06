import textwrap
import tkinter


class Field(object):

    def __init__(self):
        pass

    def get_mif():
        raise JoommfError("A class based on Field must define"
                          "it's own get_mif() function")


class RandomField(Field):

    def __init__(self, min_norm=1, max_norm=1):
        self.min_norm = min_norm
        self.max_norm = max_norm

    def get_mif(self):
        return textwrap.dedent("""\
        Oxs_RandomVectorField {
        min_norm {}
        max_norm {}
        }
        """).format(self.min_norm, self.max_norm)


class ScriptField(Field):

    def __init__(self):
        self.evaluator = tkinter.Tcl()

    def get_m0(self, scriptname):
        m0 = textwrap.dedent("""\
        Oxs_ScriptVectorField {{
        atlas :atlas
        script {}
        norm  1
        }}
        """).format(scriptname)
        return m0


class Vortex(ScriptField):

    def get_mif(self):
        self.scriptname = "Vortex"
        self.m0 = self.get_m0(self.scriptname)
        self.script = ("""\
proc Vortex {x y z} {
set yrad [expr {2.*$y-1.}]
set zrad [expr {2.*$z-1.}]
set normsq [expr {$yrad*$yrad+$zrad*$zrad}]
if {$normsq <= 0.05} {return "1 0 0"}
return [list 0.0 $zrad [expr {-1*$yrad}]]
}
""")
        return self.script, self.m0

    def values(self, x, y, z):
        _, _ = self.get_mif()
        self.evaluator.tk.eval(self.script)
        TclResult = self.evaluator.tk.eval("{} {} {} {}".format(
            self.scriptname,
            x, y, z))
        return [float(i) for i in TclResult.split()]
