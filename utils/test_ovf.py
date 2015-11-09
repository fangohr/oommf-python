import os


def test_can_import():
    import ovf
    ovf
    import lattice
    lattice


def test_example_docstring_write(tmpdir):
    from ovf import OVFFile, OVF10, OVF20
    from lattice import FieldLattice

    # Create the data
    fl = FieldLattice("2.5e-9,97.5e-9,20/2.5e-9,47.5e-9,10/2.5e-9,7.5e-9,1")

    def setter_function(position):
        return [1, 0, 0]
    fl.set(setter_function)

    # Save it to file, with OVF2 format
    ovf = OVFFile()
    ovf.new(fl, version=OVF20, data_type="binary8")
    path = os.path.join(str(tmpdir), "newfile.ovf")
    ovf.write(path)
    ovf.write("test.ovf")
    assert os.path.exists(path)
    filecontent = open(path).read()
    assert filecontent.startswith("""# OOMMF OVF 2.0
# Segment count: 1
# Begin: Segment
# Begin: Header
# Title: Title""")

    ovf = OVFFile()
    ovf.new(fl, version=OVF10, data_type="binary8")
    path = os.path.join(str(tmpdir), "newfile.ovf")
    ovf.write(path)
    ovf.write("test.ovf")
    assert os.path.exists(path)
    filecontent = open(path).read()
    assert filecontent.startswith("""# OOMMF: rectangular mesh v1.0
# Segment count: 1
# Begin: Segment
# Begin: Header
# Title: Title
# meshtype: rectangular
# meshunit: 1.0""")
