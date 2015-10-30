import oommfmif as o


def test_get_oommf_version_return_type():
    assert isinstance(o.get_version(), str)


def test_get_oommf_version():
    assert o.get_version()[0:4] == "1.2."


def test_get_oommf_path():
    assert isinstance(o.get_oommf_path(), str)
