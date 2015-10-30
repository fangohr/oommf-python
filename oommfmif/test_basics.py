import oommfmif as o


def test_get_oommf_version_return_type():
    assert isinstance(o.get_version(), str)


def test_get_oommf_version():
    assert o.get_version()[0:4] == "1.2."


def test_get_oommf_path():
    assert isinstance(o.get_oommf_path(), str)

def test_run_oommf_simulation():
    import os.path
    process = o.call_oommf('boxsi bigbar.mif')
    process.wait()
    assert os.path.exists('bigbar-Oxs_TimeDriver-Magnetization-00-0003100.omf')
        
