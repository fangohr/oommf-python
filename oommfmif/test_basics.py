import oommfmif as o


def test_get_oommf_version():
    assert isinstance(o.get_version(), str)
