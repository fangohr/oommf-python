from __future__ import unicode_literals
from builtins import bytes, str
from io import open
import os
import sys

import numpy as np
import pytest


@pytest.mark.xfail
def test_python_is_2():
    print("ovf2.py is not yet Python 3 compatible")
    assert sys.version_info[0:2] == (2, 7)


def test_can_import():
    import ovf
    ovf
    import lattice
    lattice


@pytest.fixture
def field1():
    from lattice import FieldLattice

    # Create the data
    fl = FieldLattice(
        "2.5e-9, 97.5e-9, 20/2.5e-9, 47.5e-9, 10/2.5e-9, 7.5e-9, 1")

    def setter_function(position):
        return [1, 2, 3]
    fl.set(setter_function)
    return fl


def test_example_docstring_write_ovff20(tmpdir, field1):
    from ovf import OVFFile, OVF20
    fl = field1
    # Save it to file, with OVF2 format
    ovf = OVFFile()
    ovf.new(fl, version=OVF20, data_type="binary8")
    path = os.path.join(str(tmpdir), "newfile.ovf")
    ovf.write(path)
    assert os.path.exists(path)
    filecontent = open(path, encoding='ISO-8859-1').read()
    assert filecontent.startswith("""# OOMMF OVF 2.0
# Segment count: 1
# Begin: Segment
# Begin: Header
# Title: Title""")
    # for reading test
    ovf.write("tmp_test_ovf2.ovf")


def test_example_docstring_write_ovff10(tmpdir, field1):
    from ovf import OVFFile, OVF10
    fl = field1
    ovf = OVFFile()
    ovf.new(fl, version=OVF10, data_type="binary8")
    path = os.path.join(str(tmpdir), "newfile.ovf")
    ovf.write(path)
    ovf.write("tmp_test_ovf1.ovf")
    assert os.path.exists(path)
    filecontent = open(path, encoding='ISO-8859-1').read()
    assert filecontent.startswith("""# OOMMF: rectangular mesh v1.0
# Segment count: 1
# Begin: Segment
# Begin: Header
# Title: Title
# meshtype: rectangular
# meshunit: 1.0""")


def test_example_docstring_read_ovf_file_ovf1():
    from ovf import OVFFile, OVF10
    ovf_file = OVFFile("tmp_test_ovf1.ovf")
    assert ovf_file.content.ovf_version == OVF10
    fl = ovf_file.get_field()
    assert fl.field_dim == 3
    assert np.allclose(fl.field_data[0, :, :, 0], 1.)
    assert np.allclose(fl.field_data[1, :, :, 0], 2.)
    assert np.allclose(fl.field_data[2, :, :, 0], 3.)


def test_example_docstring_read_ovf_file_ovf2():
    from ovf import OVFFile, OVF20
    ovf_file = OVFFile("tmp_test_ovf2.ovf")
    assert ovf_file.content.ovf_version == OVF20
    fl = ovf_file.get_field()
    assert fl.field_dim == 3
    assert np.allclose(fl.field_data[0, :, :, 0], 1.)
    assert np.allclose(fl.field_data[1, :, :, 0], 2.)
    assert np.allclose(fl.field_data[2, :, :, 0], 3.)

    # fl is a FieldLattice object, see module lattice.py
    # fl.lattice is a Lattice object, describing the mesh (lattice.py)
    #  fl.field_data is the numpy array containing the data
